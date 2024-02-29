const setCookie = (key, value, expiredDays) => {
 // 자동 삭제 날짜를 지정하는 코드
  let today = new Date();
  today.setDate(today.getDate() + expiredDays);
 // 쿠키에 값을 저장
  document.cookie =
    key +
    '=' +
    JSON.stringify(value) +
    '; path=/; expires=' +
    today.toGMTString() +
    ';';
};

function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) {
          var cookieValue = decodeURIComponent(c.substring(nameEQ.length, c.length));
          return cookieValue.replace(/^"|"$/g, '');
      }
  }
  return null;
}