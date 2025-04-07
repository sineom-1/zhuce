// 页面首次加载，最早检查是否已有其他窗口
(async function() {
  try {
    // 在页面内容显示前先检查是否已有窗口
    if (isStandaloneWindow && window.location.href.includes('popup.html')) {
      // 获取当前窗口ID
      const currentWindow = await new Promise(resolve => {
        chrome.windows.getCurrent(win => resolve(win));
      });
      
      // 检查是否已有其他窗口
      const response = await new Promise(resolve => {
        chrome.runtime.sendMessage({action: "checkExistingPopup"}, resp => resolve(resp));
      });
      
      if (response && response.exists && response.windowId && response.windowId !== currentWindow.id) {
        // 先聚焦现有窗口
        await new Promise(resolve => {
          chrome.runtime.sendMessage({action: "focusPopup"}, resp => resolve(resp));
        });
        
        // 立即关闭当前窗口，不显示任何内容
        window.close();
        return; // 阻止页面内容加载
      }
    }
  } catch (error) {
    // 错误处理
  }
})();

// API接口配置
const API_ENDPOINTS = {
  // 生产环境
  production: 'https://cursor.idfairy.com',
  // 本地开发环境
  development: 'http://localhost:8080',
  // 备用环境（如果需要的话）
  backup: 'http://127.0.0.1:8080'
};

// 默认使用生产环境
const API_HOST = API_ENDPOINTS.production;
const API_BOARDING_URL = `${API_HOST}/api/boarding`;
const API_CORS_TEST_URL = `${API_HOST}/api/cors-test`;
const API_NAVIGATION_URL = `${API_HOST}/api/navigation`;

// 检查是否在独立窗口中运行
const isStandaloneWindow = window.opener === null;

// 窗口检查标志，防止重复检查关闭窗口
let hasWindowBeenChecked = false;

// 获取操作系统平台信息
function getPlatform() {
  const userAgent = navigator.userAgent;
  
  if (userAgent.indexOf("Win") !== -1) return "Windows";
  if (userAgent.indexOf("Mac") !== -1) return "macOS";
  if (userAgent.indexOf("Linux") !== -1) return "Linux";
  if (userAgent.indexOf("Android") !== -1) return "Android";
  if (userAgent.indexOf("iOS") !== -1 || userAgent.indexOf("iPhone") !== -1 || userAgent.indexOf("iPad") !== -1) return "iOS";
  
  return "Unknown";
}

// 获取TLS指纹数据
async function getTlsData() {
  try {
    const response = await fetch('https://tls.browserleaks.com/json', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`获取TLS数据失败，HTTP状态码: ${response.status}`);
    }
    
    const data = await response.json();
    
    // 只返回 user_agent 和 akamai_hash
    return {
      user_agent: data.user_agent,
      akamai_hash: data.akamai_hash
    };
  } catch (error) {
    // 获取失败时返回基本信息，避免整个流程失败
    return {
      user_agent: navigator.userAgent,
      akamai_hash: '',
      error: "获取TLS数据失败: " + error.message,
      timestamp: Date.now(),
      platform: getPlatform()
    };
  }
}

// 处理响应结果
function handleResponse(data) {
  const btnSpinner = document.getElementById('btn-spinner');
  const btnText = document.getElementById('btn-text');
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('status-text');
  const submitBtn = document.getElementById('submit-btn');
  const ticketInput = document.getElementById('ticket'); // 获取输入框引用
  const navContainer = document.getElementById('nav-links-container');
  
  // 处理响应结果
  if (data.code === 0) {
    // 上车成功，显示庆祝界面
    showSuccessAnimation();
    // 成功界面不需要恢复输入框状态，因为界面已被替换
    
    // 清除认证参数，防止重复使用
    try {
      chrome.runtime.sendMessage({action: "clearAuthParams"}, (response) => {
        // 清除认证参数
      });
    } catch (error) {
      // 清除认证参数失败
    }
  } else {
    // 上车失败，显示错误信息
    btnSpinner.style.display = 'none';
    btnText.textContent = '立即上车';
    statusDiv.style.display = 'block';
    
    // 隐藏导航链接
    if (navContainer) {
      navContainer.style.display = 'none';
    }
    
    // 显示服务器返回的错误消息
    const errorMessage = data.message || '未知错误';
    statusText.textContent = '上车失败: ' + errorMessage;
    statusText.style.color = '#ff0000'; // 红色文字
    statusDiv.style.backgroundColor = '#e2e2e2';
    submitBtn.disabled = false;
    ticketInput.disabled = false; // 恢复输入框状态
    
    // 3秒后隐藏状态并恢复导航链接显示
    setTimeout(() => {
      statusDiv.style.display = 'none';
      
      // 重新显示导航链接
      if (navContainer) {
        navContainer.style.display = 'flex';
      }
    }, 3000);
  }
}

// 显示成功动画和彩带效果
function showSuccessAnimation() {
  // 获取主界面容器
  const container = document.querySelector('.container');
  if (!container) return;
  
  // 清空容器内容
  container.innerHTML = '';
  
  // 创建成功页面元素
  const successDiv = document.createElement('div');
  successDiv.className = 'success-container';
  successDiv.style.cssText = `
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 260px;
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
  `;
  
  // 添加成功图标
  const iconDiv = document.createElement('div');
  iconDiv.className = 'success-icon';
  iconDiv.style.cssText = `
    margin-bottom: 20px;
    width: 100px;
    height: 100px;
    background-image: url('./images/popper.webp');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  `;
  
  // 添加成功标题
  const titleDiv = document.createElement('div');
  titleDiv.className = 'success-title';
  titleDiv.style.cssText = `
    font-size: 20px;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
  `;
  titleDiv.textContent = '上车成功！';
  
  // 添加唤起客户端按钮
  const launchBtn = document.createElement('a');
  launchBtn.href = 'cursor://';
  launchBtn.className = 'launch-btn';
  launchBtn.style.cssText = `
    display: inline-block;
    background-color: #23ff00;
    color: black;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    margin-top: 10px;
    cursor: pointer;
  `;
  launchBtn.textContent = '返回Cursor客户端';
  launchBtn.onclick = function(e) {
    // 让链接正常工作，不需要阻止默认行为
  };
  
  // 将元素添加到成功页面
  successDiv.appendChild(iconDiv);
  successDiv.appendChild(titleDiv);
  successDiv.appendChild(launchBtn);
  
  // 添加到容器
  container.appendChild(successDiv);
  
  // 设置容器最小高度和圆角
  const style = document.createElement('style');
  style.textContent = `
    .container {
      min-height: 260px;
      overflow: hidden;
    }
    body {
      overflow: hidden;
    }
    html {
      overflow: hidden;
    }
  `;
  document.head.appendChild(style);
  
  // 延迟1秒后尝试唤起Cursor客户端
  setTimeout(() => {
    try {
      // 多种方式尝试打开cursor://协议链接
      // 方法1: window.open
      const newWindow = window.open('cursor://', '_blank');
      
      // 方法2: 如果window.open返回null或被阻止，使用iframe方法
      if (!newWindow) {
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = 'cursor://';
        document.body.appendChild(iframe);
        setTimeout(() => {
          document.body.removeChild(iframe);
        }, 100);
      }
    } catch (error) {
      // 唤起失败
    }
  }, 1000);
}

// 校验输入并更新按钮状态
function validateInput() {
  const ticketInput = document.getElementById('ticket');
  const submitBtn = document.getElementById('submit-btn');
  
  if (!ticketInput) {
    return;
  }
  
  if (!submitBtn) {
    return;
  }
  
  const ticketValue = ticketInput.value.trim();
  
  const shouldDisable = ticketValue === '';
  
  if (shouldDisable) {
    submitBtn.disabled = true;
  } else {
    submitBtn.disabled = false;
    
    // 强制更新按钮样式
    submitBtn.style.opacity = '1';
    submitBtn.style.cursor = 'pointer';
  }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', async function() {
  // 添加圆角样式
  const roundedStyle = document.createElement('style');
  roundedStyle.textContent = `
    html, body {
      overflow: hidden;
    }
    .container {
      overflow: hidden;
    }
  `;
  document.head.appendChild(roundedStyle);
  
  const submitBtn = document.getElementById('submit-btn');
  const ticketInput = document.getElementById('ticket');
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('status-text');
  
  // 初始禁用按钮
  if (submitBtn) {
    submitBtn.disabled = true;
  }
  
  // 确保在初始化时就添加输入监听事件，并立即检查
  if (ticketInput) {
    // 添加多种事件监听，确保能捕获到用户输入
    ticketInput.addEventListener('input', validateInput);
    ticketInput.addEventListener('change', validateInput);
    ticketInput.addEventListener('keyup', validateInput);
    
    // 立即运行一次验证以确保初始状态正确
    validateInput();
  }
  
  // 添加缺失的初始化认证方法
  await initializeAuthentication();
  
  // 再次确认按钮状态
  setTimeout(() => {
    if (submitBtn) {
      // 重新验证一次输入以确保状态正确
      validateInput();
    }
  }, 2000);
});

// 使用预先缓存的TLS数据发送到服务器
async function sendToServerWithCachedTls(challenge, uuid, ticket, platform, cachedTlsData) {
  const btnSpinner = document.getElementById('btn-spinner');
  const btnText = document.getElementById('btn-text');
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('status-text');
  const submitBtn = document.getElementById('submit-btn');
  const ticketInput = document.getElementById('ticket');
  
  // 显示加载状态
  btnSpinner.style.display = 'block';
  btnText.textContent = '正在上车...';
  submitBtn.disabled = true;
  ticketInput.disabled = true; // 禁用输入框
  statusDiv.style.display = 'none';
  
  try {
    if (!uuid || !challenge) {
      showStatus('系统错误: 缺少UUID或Challenge', false);
      return;
    }
    
    // 使用预先获取的TLS数据，如果没有则重新获取
    let tlsData = cachedTlsData;
    if (!tlsData) {
      tlsData = await getTlsData();
    } else {
      // 确保缓存的TLS数据只包含user_agent和akamai_hash
      tlsData = {
        user_agent: tlsData.user_agent,
        akamai_hash: tlsData.akamai_hash || ''
      };
    }
    
    // 构建请求数据
    const requestData = {
      challenge,
      uuid,
      ticket,
      platform,
      tls: tlsData,
      timestamp: Date.now()
    };
    
    // 使用mode: 'cors'明确指定这是跨域请求
    const fetchOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors', // 明确指定跨域模式
      body: JSON.stringify(requestData)
    };
    
    try {
      const response = await fetch(API_BOARDING_URL, fetchOptions);
      
      // 无论状态码如何，都尝试解析响应体
      let responseText = await response.text();
      
      let responseData;
      try {
        // 尝试将响应解析为JSON
        if (responseText) {
          responseData = JSON.parse(responseText);
        }
      } catch (jsonError) {
        // 解析JSON失败
      }
      
      // 处理错误状态码
      if (!response.ok) {
        if (responseData && responseData.message) {
          // 使用服务器返回的错误消息
          throw new Error(responseData.message);
        } else if (responseText) {
          // 如果有响应体但不是有效的JSON，直接显示文本
          throw new Error(`服务器返回错误: ${responseText}`);
        } else {
          // 没有任何有用的错误信息，使用HTTP状态
          throw new Error(`HTTP请求失败，状态码: ${response.status}, ${response.statusText}`);
        }
      }
      
      // 如果状态码正常，但服务器依然返回了错误码
      if (responseData && responseData.code !== 0) {
        // 直接使用handleResponse处理这种情况，它会显示错误消息
        handleResponse(responseData);
      } else if (responseData) {
        // 正常成功的响应
        handleResponse(responseData);
      } else {
        // 无响应数据
        throw new Error('服务器没有返回有效数据');
      }
    } catch (fetchError) {
      // 获取导航容器
      const navContainer = document.getElementById('nav-links-container');
      
      // 隐藏导航链接
      if (navContainer) {
        navContainer.style.display = 'none';
      }
      
      // 显示错误
      statusDiv.style.display = 'block';
      statusText.textContent = fetchError.message;
      statusText.style.color = '#ff0000'; // 红色文字
      statusDiv.style.backgroundColor = '#e2e2e2';
      
      // 3秒后隐藏状态并恢复导航链接显示
      setTimeout(() => {
        statusDiv.style.display = 'none';
        
        // 重新显示导航链接
        if (navContainer) {
          navContainer.style.display = 'flex';
        }
      }, 3000);
      
      // 恢复按钮状态
      btnSpinner.style.display = 'none';
      btnText.textContent = '立即上车';
      submitBtn.disabled = false;
      ticketInput.disabled = false;
    }
    
  } catch (error) {
    // 获取导航容器
    const navContainer = document.getElementById('nav-links-container');
    
    // 隐藏导航链接
    if (navContainer) {
      navContainer.style.display = 'none';
    }
    
    // 隐藏加载状态，显示错误
    btnSpinner.style.display = 'none';
    btnText.textContent = '立即上车';
    statusDiv.style.display = 'block';
    statusText.textContent = '请求失败: ' + error.message;
    statusText.style.color = '#ff0000'; // 红色文字
    statusDiv.style.backgroundColor = '#e2e2e2';
    submitBtn.disabled = false;
    ticketInput.disabled = false; // 恢复输入框状态
    
    // 3秒后隐藏状态并恢复导航链接显示
    setTimeout(() => {
      statusDiv.style.display = 'none';
      
      // 重新显示导航链接
      if (navContainer) {
        navContainer.style.display = 'flex';
      }
    }, 3000);
  }
}

// 显示状态提示函数
function showStatus(message, isSuccess) {
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('status-text');
  const navContainer = document.getElementById('nav-links-container');
  
  // 显示状态提示
  statusDiv.style.display = 'block';
  statusText.textContent = message;
  
  // 隐藏导航链接
  if (navContainer) {
    navContainer.style.display = 'none';
  }
  
  if (isSuccess) {
    statusDiv.style.backgroundColor = '#d4edda';  // 绿色背景
    statusText.style.color = '#000';  // 黑色文字
  } else {
    statusDiv.style.backgroundColor = '#e2e2e2';  // 灰色背景
    statusText.style.color = '#ff0000';  // 红色文字
  }
  
  // 显示3秒后隐藏状态提示并重新显示导航链接
  setTimeout(() => {
    statusDiv.style.display = 'none';
    
    // 重新显示导航链接
    if (navContainer) {
      navContainer.style.display = 'flex';
    }
  }, 3000);
}

// 获取导航链接并显示
async function fetchNavigationLinks() {
  try {
    const response = await fetch(API_NAVIGATION_URL);
    if (!response.ok) {
      return;
    }
    
    const data = await response.json();
    if (data.code === 0 && Array.isArray(data.data)) {
      renderNavigationLinks(data.data);
    }
  } catch (error) {
    // 获取导航链接出错
  }
}

// 渲染导航链接
function renderNavigationLinks(links) {
  // 如果没有链接，不显示导航区域
  if (!links || links.length === 0) {
    return;
  }
  
  // 获取或创建导航容器
  let navContainer = document.getElementById('nav-links-container');
  if (!navContainer) {
    navContainer = document.createElement('div');
    navContainer.id = 'nav-links-container';
    navContainer.style.cssText = `
      display: flex;
      justify-content: center;
      margin-top: 15px;
      gap: 20px;
      flex-wrap: wrap;
    `;
    
    // 将导航容器插入到提交按钮之后
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn && submitBtn.parentNode) {
      submitBtn.parentNode.insertBefore(navContainer, submitBtn.nextSibling);
    } else {
      document.body.appendChild(navContainer);
    }
  }
  
  // 清空现有导航链接
  navContainer.innerHTML = '';
  
  // 添加新的导航链接
  links.forEach(link => {
    const linkElement = document.createElement('a');
    linkElement.href = link.url;
    linkElement.target = '_blank'; // 在新标签页中打开
    linkElement.textContent = link.text;
    linkElement.style.cssText = `
      color: #888;
      text-decoration: none;
      font-size: 12px;
      transition: color 0.2s;
    `;
    
    // 鼠标悬停效果
    linkElement.addEventListener('mouseover', () => {
      linkElement.style.color = '#555';
    });
    
    linkElement.addEventListener('mouseout', () => {
      linkElement.style.color = '#888';
    });
    
    navContainer.appendChild(linkElement);
  });
}

// 初始化表单处理
function setupForm() {
  const form = document.getElementById('boarding-form');
  const submitBtn = document.getElementById('submit-btn');
  const ticketInput = document.getElementById('ticket');
  
  if (form) {
    // 监听表单提交事件
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const ticket = ticketInput.value.trim();
      
      if (ticket) {
        submitBtn.click();
      } else {
        validateInput(); // 再次验证以确保按钮状态正确
      }
    });
  }
  
  // 确保输入事件被正确处理
  if (ticketInput) {
    ['input', 'change', 'keyup'].forEach(eventType => {
      ticketInput.addEventListener(eventType, function() {
        validateInput();
      });
    });
    
    // 特别处理Enter键
    ticketInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        
        if (ticketInput.value.trim()) {
          if (!submitBtn.disabled) {
            submitBtn.click();
          } else {
            submitBtn.disabled = false;
            submitBtn.click();
          }
        }
      }
    });
  }
}

// 添加缺失的初始化认证方法
async function initializeAuthentication() {
  // 预先获取TLS数据
  let cachedTlsData = null;
  try {
    cachedTlsData = await getTlsData();
  } catch (error) {
    // 获取失败时继续执行，sendToServerWithCachedTls函数内部会处理空的TLS数据
  }
  
  // 从URL获取参数
  let challenge = null;
  let uuid = null;
  let isFromDeepControl = false;
  
  // 尝试直接从location.href解析参数
  function parseParamsFromFullUrl(fullUrl) {
    try {
      const urlObj = new URL(fullUrl);
      return {
        challenge: urlObj.searchParams.get('challenge'),
        uuid: urlObj.searchParams.get('uuid'),
        fromDeepControl: urlObj.searchParams.get('fromDeepControl')
      };
    } catch (e) {
      return null;
    }
  }
  
  // 方法1: 直接从完整URL解析
  const parsedFromFull = parseParamsFromFullUrl(window.location.href);
  
  // 方法2: 标准方式解析search部分
  try {
    const searchParams = new URLSearchParams(window.location.search);
    
    challenge = searchParams.get('challenge');
    uuid = searchParams.get('uuid');
    const fromDeepControl = searchParams.get('fromDeepControl');
    
    // 检查是否有合法的参数和来源标识
    if (challenge && uuid && fromDeepControl === 'true' && isStandaloneWindow) {
      isFromDeepControl = true;
    }
  } catch (e) {
    // 解析URL参数出错
  }
  
  // 方法3: 手动解析URL查询参数
  function parseQueryString(queryString) {
    if (!queryString || queryString === '') return {};
    
    // 确保移除开头的问号
    if (queryString.startsWith('?')) {
      queryString = queryString.substring(1);
    }
    
    const params = {};
    const segments = queryString.split('&');
    
    for (let i = 0; i < segments.length; i++) {
      const parts = segments[i].split('=');
      if (parts.length === 2) {
        const key = decodeURIComponent(parts[0]);
        const value = decodeURIComponent(parts[1]);
        params[key] = value;
      }
    }
    
    return params;
  }
  
  const manualParams = parseQueryString(window.location.search);
  
  // 如果方法3找到了有效参数，尝试使用
  if (manualParams.challenge && manualParams.uuid && manualParams.fromDeepControl === 'true' && isStandaloneWindow) {
    challenge = manualParams.challenge;
    uuid = manualParams.uuid;
    isFromDeepControl = true;
  }
  
  // 如果URL中有完整参数，尝试再次验证parsedFromFull结果
  if (!challenge && parsedFromFull && parsedFromFull.challenge && parsedFromFull.uuid) {
    challenge = parsedFromFull.challenge;
    uuid = parsedFromFull.uuid;
    isFromDeepControl = parsedFromFull.fromDeepControl === 'true' && isStandaloneWindow;
  }
  
  // 通过document.referrer检查来源URL
  if (document.referrer) {
    try {
      const referrerUrl = new URL(document.referrer);
      // 检查来源
    } catch (e) {
      // 解析referrer URL失败
    }
  }
  
  // 如果从URL未获取到参数，从storage获取
  if (!challenge || !uuid || !isFromDeepControl) {
    try {
      const result = await new Promise((resolve) => {
        chrome.storage.local.get('authParams', (data) => {
          resolve(data);
        });
      });
      
      // 更详细地检查storage中的数据
      if (result && result.authParams) {
        const storageTimestamp = result.authParams.timestamp || 0;
        const now = Date.now();
        const timeDiff = now - storageTimestamp;
        
        if (timeDiff <= 10000 && result.authParams.fromDeepControl === true) {
          challenge = result.authParams.challenge;
          uuid = result.authParams.uuid;
          isFromDeepControl = true;
        }
      }
    } catch (error) {
      // 获取storage数据时出错
    }
  }
  
  // 检查是否获取到了必要参数且来源合法
  if (!challenge || !uuid || !isFromDeepControl) {
    showStatus('请从Cursor客户端点击登录', false);
    
    // 禁用输入框和按钮
    const ticketInput = document.getElementById('ticket');
    const submitBtn = document.getElementById('submit-btn');
    if (ticketInput) ticketInput.disabled = true;
    if (submitBtn) submitBtn.disabled = true;
    
    // 清除任何可能存在的参数
    try {
      chrome.runtime.sendMessage({action: "clearAuthParams"}, (response) => {
        // 已请求清除所有认证参数
      });
    } catch (error) {
      // 清除参数失败
    }
    
    return;
  }
  
  // 添加表单处理
  setupForm();
  
  // 如果获取到了有效参数，预先准备TLS数据
  getTlsDataAndPrepareSubmit(challenge, uuid);
  
  // 获取导航链接
  fetchNavigationLinks();
}

// 添加缺失的方法
async function getTlsDataAndPrepareSubmit(challenge, uuid) {
  // 预先获取TLS数据
  let cachedTlsData = null;
  try {
    cachedTlsData = await getTlsData();
  } catch (error) {
    // 获取TLS数据出错
  }
  
  const authParams = {
    challenge: challenge,
    uuid: uuid,
    timestamp: Date.now()
  };
  
  // 再次检查和设置按钮状态
  const submitBtn = document.getElementById('submit-btn');
  const ticketInput = document.getElementById('ticket');
  
  // 强制检查验证
  validateInput();
  
  // 绑定提交按钮点击事件
  submitBtn.addEventListener('click', async function() {
    const ticketInput = document.getElementById('ticket');
    const ticket = ticketInput.value.trim();
    
    if (ticket === '') {
      // 显示错误提示
      showStatus('请输入车票', false);
      return;
    }
    
    // 发送请求，使用预先获取的TLS数据
    sendToServerWithCachedTls(
      authParams.challenge,
      authParams.uuid,
      ticket,
      getPlatform(),
      cachedTlsData
    );
  });
  
  // 监听输入操作，确保每次键入都更新按钮状态
  ticketInput.addEventListener('input', validateInput);
  ticketInput.addEventListener('change', validateInput);
  ticketInput.addEventListener('keyup', validateInput);
  
  // 设置表单提交监听，防止按钮不起作用
  const form = ticketInput.closest('form');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      if (!submitBtn.disabled) {
        submitBtn.click();
      }
    });
  }
  
  // 延迟200ms后再检查一次按钮状态
  setTimeout(() => {
    validateInput();
    
    // 强制按钮样式更新
    if (ticketInput.value.trim() !== '') {
      submitBtn.disabled = false;
      submitBtn.style.opacity = '1';
      submitBtn.style.cursor = 'pointer';
    }
  }, 200);
} 