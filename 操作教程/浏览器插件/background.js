let popupWindowId = null;

// 清除认证参数
function clearAuthParams(callback) {
  chrome.storage.local.remove('authParams', () => {
    if (callback) callback({success: true});
  });
}

// 存储认证参数
function storeAuthParams(params, callback) {
  chrome.storage.local.set({authParams: params}, () => {
    if (callback) callback({success: true});
  });
}

// 检查窗口是否存在
async function windowExists(windowId) {
  if (!windowId) return false;
  
  try {
    const window = await chrome.windows.get(windowId);
    return !!window;
  } catch (error) {
    return false;
  }
}

// 关闭现有窗口
async function closeExistingPopup() {
  if (popupWindowId !== null) {
    try {
      const exists = await windowExists(popupWindowId);
      if (exists) {
        await chrome.windows.remove(popupWindowId);
      }
    } catch (error) {
      // 关闭窗口时出错
    }
    popupWindowId = null;
  }
}

// 创建独立弹出窗口
async function createPopupWindow(url) {
  try {
    // 先尝试关闭现有窗口
    await closeExistingPopup();
    
    // 创建新窗口之前，先确认没有其他popup.html窗口
    const allWindows = await chrome.windows.getAll();
    
    for (const win of allWindows) {
      try {
        const tabs = await chrome.tabs.query({windowId: win.id});
        
        for (const tab of tabs) {
          if (tab.url && tab.url.includes('popup.html')) {
            try {
              await chrome.windows.remove(win.id);
            } catch (removeError) {
              // 关闭其他popup窗口失败
            }
            break;
          }
        }
      } catch (queryError) {
        // 查询窗口标签页失败
      }
    }
    
    // 创建新窗口
    const popup = await chrome.windows.create({
      url: url,
      type: 'popup',
      width: 280,
      height: 430,
      focused: true
    });
    
    popupWindowId = popup.id;
    
    // 监听窗口关闭
    chrome.windows.onRemoved.addListener(function windowClosedListener(windowId) {
      if (windowId === popupWindowId) {
        popupWindowId = null;
        chrome.windows.onRemoved.removeListener(windowClosedListener);
      }
    });
    
    return popup;
  } catch (error) {
    // 创建弹出窗口时出错
    return null;
  }
}

// 监听消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "clearAuthParams") {
    clearAuthParams(sendResponse);
    return true; // 保持通道开放，异步发送响应
  } 
  
  if (request.action === "storeAuthParams") {
    storeAuthParams(request.params, sendResponse);
    return true; // 保持通道开放，异步发送响应
  }
  
  if (request.action === "createPopup") {
    if (request.params && request.params.challenge && request.params.uuid) {
      // 先检查是否已有弹窗
      windowExists(popupWindowId).then(async exists => {
        if (exists) {
          try {
            await chrome.windows.update(popupWindowId, {focused: true});
            
            // 存储最新参数
            storeAuthParams({
              challenge: request.params.challenge,
              uuid: request.params.uuid,
              fromDeepControl: true,
              timestamp: Date.now()
            });
            
            // 返回已有窗口信息
            sendResponse({success: true, windowId: popupWindowId, reused: true});
          } catch (error) {
            // 聚焦失败，窗口可能已关闭但引用未更新
            popupWindowId = null;
            // 尝试创建新窗口
            createNewPopup();
          }
        } else {
          // 没有现有窗口或窗口已关闭，先重置窗口ID
          if (popupWindowId !== null) {
            popupWindowId = null;
          }
          // 创建新窗口
          createNewPopup();
        }
      });
      
      async function createNewPopup() {
        // 存储参数
        storeAuthParams({
          challenge: request.params.challenge,
          uuid: request.params.uuid,
          fromDeepControl: true,
          timestamp: Date.now()
        });
        
        // 构建URL
        const url = chrome.runtime.getURL("popup.html") + 
          `?challenge=${encodeURIComponent(request.params.challenge)}` +
          `&uuid=${encodeURIComponent(request.params.uuid)}` +
          `&fromDeepControl=true`;
        
        // 创建弹出窗口
        try {
          const popup = await createPopupWindow(url);
          sendResponse({success: !!popup, windowId: popup ? popup.id : null, reused: false});
        } catch (error) {
          sendResponse({success: false, error: error.message});
        }
      }
      
      return true; // 保持通道开放，异步发送响应
    } else {
      sendResponse({success: false, error: '缺少必要参数'});
    }
  }
  
  if (request.action === "checkExistingPopup") {
    windowExists(popupWindowId).then(exists => {
      sendResponse({exists, windowId: exists ? popupWindowId : null});
    });
    return true; // 保持通道开放，异步发送响应
  }
  
  if (request.action === "focusPopup") {
    if (popupWindowId !== null) {
      windowExists(popupWindowId).then(exists => {
        if (exists) {
          chrome.windows.update(popupWindowId, {focused: true}).then(() => {
            sendResponse({success: true});
          }).catch(error => {
            // 聚焦失败，可能窗口已关闭，重置窗口ID
            popupWindowId = null;
            sendResponse({success: false, error: error.message});
          });
        } else {
          popupWindowId = null;
          sendResponse({success: false, error: '弹窗不存在'});
        }
      });
      return true; // 保持通道开放，异步发送响应
    } else {
      sendResponse({success: false, error: '没有活动的弹窗'});
    }
  }
});

// 监听窗口创建事件，检测是否是popup.html窗口
chrome.windows.onCreated.addListener(async (window) => {
  try {
    // 如果已有窗口存在，先检查它是否有效
    if (popupWindowId !== null) {
      const existingWindowExists = await windowExists(popupWindowId);
      if (!existingWindowExists) {
        popupWindowId = null;
      }
    }
    
    // 获取窗口中的标签页
    const tabs = await chrome.tabs.query({windowId: window.id});
    let isPopupWindow = false;
    
    // 检查新窗口是否含有popup.html页面
    for (const tab of tabs) {
      if (tab.url && tab.url.includes('popup.html')) {
        isPopupWindow = true;
        break;
      }
    }
    
    if (isPopupWindow) {
      // 如果没有已记录的窗口，记录这个新窗口
      if (popupWindowId === null) {
        popupWindowId = window.id;
      } 
      // 如果已有窗口且不是当前窗口
      else if (window.id !== popupWindowId) {
        // 直接关闭新窗口，不等待用户看到，避免闪现
        try {
          await chrome.windows.remove(window.id);
        } catch (error) {
          // 如果新窗口无法关闭，尝试聚焦到现有窗口
          try {
            await chrome.windows.update(popupWindowId, {focused: true});
          } catch (focusError) {
            // 如果现有窗口无法聚焦，说明可能已经关闭，使用新窗口
            popupWindowId = window.id;
          }
        }
      }
    }
  } catch (error) {
    // 处理窗口创建事件时出错
  }
});

// 监听标签页更新事件，处理URL变更的情况
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.includes('popup.html')) {
    chrome.windows.get(tab.windowId).then(window => {
      if (window.type === 'popup') {
        // 检查是否已有其他弹窗窗口
        if (popupWindowId !== null && tab.windowId !== popupWindowId) {
          windowExists(popupWindowId).then(exists => {
            if (exists) {
              chrome.windows.update(popupWindowId, {focused: true}).then(() => {
                setTimeout(() => {
                  chrome.windows.remove(tab.windowId).catch(error => {
                    // 关闭窗口失败
                  });
                }, 300);
              }).catch(error => {
                // 现有窗口无法聚焦，使用新窗口
                popupWindowId = tab.windowId;
              });
            } else {
              // 现有窗口引用无效，更新为新窗口
              popupWindowId = tab.windowId;
            }
          });
        } else if (popupWindowId === null) {
          // 没有记录的窗口，记录这个窗口
          popupWindowId = tab.windowId;
        }
      }
    }).catch(error => {
      // 获取窗口信息失败
    });
  }
});

// 监听插件安装
chrome.runtime.onInstalled.addListener(() => {
  popupWindowId = null;
});

// 监听URL变化，检测登录深度控制URL
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  // 解析URL以获取主域名
  let hostname;
  try {
    const url = new URL(details.url);
    hostname = url.hostname;
  } catch (e) {
    return;
  }
  
  // 仅处理cursor.com和www.cursor.com域名下的请求
  if (!hostname.endsWith('cursor.com') || hostname === 'authenticator.cursor.sh') {
    return;
  }
  
  // 使用正则表达式匹配loginDeepControl，不依赖于特定地区路径
  if (details.url.match(/cursor\.com\/.*?\/loginDeepControl/) || 
      details.url.match(/cursor\.com\/loginDeepControl/)) {
    // 解析URL参数
    const url = new URL(details.url);
    const challenge = url.searchParams.get('challenge');
    const uuid = url.searchParams.get('uuid');
    const mode = url.searchParams.get('mode');
    
    // 如果是登录模式且有必要的参数
    if (mode === 'login' && challenge && uuid) {
      // 检查是否已有弹窗窗口
      windowExists(popupWindowId).then(async exists => {
        if (exists) {
          try {
            await chrome.windows.update(popupWindowId, {focused: true});
            
            // 更新storage中的参数
            const authParamsData = {
              challenge,
              uuid,
              timestamp: Date.now(),
              fromDeepControl: true
            };
            chrome.storage.local.set({authParams: authParamsData});
          } catch (error) {
            createDeepControlPopup();
          }
        } else {
          createDeepControlPopup();
        }
      });
      
      function createDeepControlPopup() {
        // 为了确保URL参数传递一致性，直接创建URL对象并添加参数
        const popupUrl = new URL(chrome.runtime.getURL('popup.html'));
        popupUrl.searchParams.set('challenge', challenge);
        popupUrl.searchParams.set('uuid', uuid);
        popupUrl.searchParams.set('fromDeepControl', 'true');
        
        // 使用createPopupWindow函数创建窗口，确保只有一个窗口实例
        createPopupWindow(`popup.html?challenge=${encodeURIComponent(challenge)}&uuid=${encodeURIComponent(uuid)}&fromDeepControl=true`).then(window => {
          if (window) {
            // 作为备份，也存储在storage中
            const authParamsData = {
              challenge,
              uuid,
              timestamp: Date.now(),
              fromDeepControl: true,  // 标记为从合法渠道打开
              windowId: window.id     // 存储窗口ID，便于验证
            };
            
            chrome.storage.local.set({
              authParams: authParamsData
            });
          }
        });
      }
    }
  }
});

// 监听重定向，确保参数不会丢失
chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
  // 解析URL以获取主域名
  let hostname;
  try {
    const url = new URL(details.url);
    hostname = url.hostname;
  } catch (e) {
    return;
  }
  
  // 检测authenticator.cursor.sh页面上的状态更改
  if (details.url.includes('authenticator.cursor.sh')) {
    // 从URL中提取原始loginDeepControl参数
    try {
      const url = new URL(details.url);
      const state = url.searchParams.get('state');
      if (state) {
        let stateObj;
        try {
          stateObj = JSON.parse(decodeURIComponent(state));
        } catch (e) {
          return;
        }
        
        // 检查returnTo的URL是否指向cursor.com
        if (stateObj.returnTo) {
          let returnToHostname;
          try {
            const returnToUrl = new URL(decodeURIComponent(stateObj.returnTo));
            returnToHostname = returnToUrl.hostname;
          } catch (e) {
            return;
          }
          
          // 仅处理返回到cursor.com域名的请求，排除authenticator.cursor.sh
          if (!returnToHostname.endsWith('cursor.com') || returnToHostname === 'authenticator.cursor.sh') {
            return;
          }
        
          if (stateObj.returnTo.match(/cursor\.com\/.*?\/loginDeepControl/) || 
              stateObj.returnTo.match(/cursor\.com\/loginDeepControl/)) {
            const returnToUrl = new URL(decodeURIComponent(stateObj.returnTo));
            const challenge = returnToUrl.searchParams.get('challenge');
            const uuid = returnToUrl.searchParams.get('uuid');
            
            if (challenge && uuid) {
              // 检查是否已有弹窗窗口
              windowExists(popupWindowId).then(async exists => {
                if (exists) {
                  try {
                    await chrome.windows.update(popupWindowId, {focused: true});
                    
                    // 更新storage中的参数
                    const authParamsData = {
                      challenge,
                      uuid,
                      timestamp: Date.now(),
                      fromDeepControl: true
                    };
                    chrome.storage.local.set({authParams: authParamsData});
                  } catch (error) {
                    createRedirectPopup();
                  }
                } else {
                  createRedirectPopup();
                }
              });
              
              function createRedirectPopup() {
                // 为了确保URL参数传递一致性，直接创建URL对象并添加参数
                const popupUrl = new URL(chrome.runtime.getURL('popup.html'));
                popupUrl.searchParams.set('challenge', challenge);
                popupUrl.searchParams.set('uuid', uuid);
                popupUrl.searchParams.set('fromDeepControl', 'true');
                
                // 使用createPopupWindow函数创建新窗口，确保只有一个窗口实例
                createPopupWindow(`popup.html?challenge=${encodeURIComponent(challenge)}&uuid=${encodeURIComponent(uuid)}&fromDeepControl=true`).then(window => {
                  if (window) {
                    // 作为备份，也存储在storage中
                    const authParamsData = {
                      challenge,
                      uuid,
                      timestamp: Date.now(),
                      fromDeepControl: true,  // 标记为从合法渠道打开
                      windowId: window.id     // 存储窗口ID，便于验证
                    };
                    
                    chrome.storage.local.set({
                      authParams: authParamsData
                    });
                  }
                });
              }
            }
          }
        }
      }
    } catch (error) {
      // 解析重定向URL参数出错
    }
  }
});

// 监听扩展程序图标点击事件，手动打开时清除之前的参数
chrome.action.onClicked.addListener((tab) => {
  // 立即清除任何可能存在的认证参数
  chrome.storage.local.remove('authParams');
});

// 监听来自popup.js的消息请求
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getAuthParams") {
    // 从storage中获取最新的授权参数
    chrome.storage.local.get(['authParams'], (result) => {
      // 只传递标记为从合法渠道打开的参数
      if (result.authParams && result.authParams.fromDeepControl) {
        // 检查时间戳，确保参数没有过期（10秒内）
        const timestamp = result.authParams.timestamp || 0;
        const now = Date.now();
        const isExpired = (now - timestamp) > 10 * 1000; // 10秒过期
        
        if (isExpired) {
          chrome.storage.local.remove('authParams');
          sendResponse({});
        } else {
          sendResponse(result);
        }
      } else {
        sendResponse({});
      }
    });
    
    // 必须返回true以使sendResponse异步工作
    return true;
  } else if (request.action === "clearAuthParams") {
    // 提供一个明确的清除参数的方法
    chrome.storage.local.remove('authParams', () => {
      sendResponse({success: true});
    });
    return true;
  }
}); 