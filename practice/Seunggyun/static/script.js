function sign_out() {
  console.log('sign_out!');
  $.removeCookie('mytoken', { path: '/' });
  alert('로그아웃!');
  window.location.href = '/';
}

function update_profile() {
  let name = $('#input-name').val()
  let file = $('#input-pic')[0].files[0]
  let form_data = new FormData()
  form_data.append("file_give", file)
  form_data.append("name_give", name)
  console.log(name, file, form_data)

  $.ajax({
    type: "POST",
    url: "/update_profile",
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response["result"] == "success") {
        alert(response["msg"])
        window.location.reload()

      }
    }
  });
}

function is_nickname(asValue) {
  var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{5,20}$/;
  return regExp.test(asValue);
}

function is_nickname2(asValue) {
  var regExp = /^[가-힣]{2,6}$/;
  return regExp.test(asValue);
}

function is_password(asValue) {
  var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{5,20}$/;
  return regExp.test(asValue);
}

function check_id() {
  let username = $('#input-username').val();

  console.log(username);
  if (username == '') {
    $('#help-id')
      .text('5~20자 이상의 한글/영문/숫자 포함 가능')
      .removeClass(' is-safe')
      .addClass('is-danger');
    $('#input-username').focus();
    return;
  }
  if (!is_nickname(username)) {
    $('#help-id')
      .text('5~20자 이상의 한글/영문/숫자 포함 가능')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-username').focus();
    return;
  }
  $('#help-id').addClass('is-loading');
  $.ajax({
    type: 'POST',
    url: '/sign_up/check_id',
    data: {
      username_give: username,
    },
    success: function (response) {
      if (response['exists']) {
        $('#help-id')
          .text('이미 존재하는 아이디입니다.')
          .removeClass('is-safe')
          .addClass('is-danger');
        $('#input-username').focus();
      } else {
        $('#help-id')
          .text('사용가능 아이디입니다.')
          .removeClass('is-danger')
          .addClass('is-success');
      }
      $('#help-id').removeClass('is-loading');
    },
  });
}

function check_nick() {
  let nickname = $('#input-nickname').val();

  if (nickname == '') {
    $('#help-nick')
      .text('2~6자이상의 한글')
      .removeClass(' is-safe')
      .addClass('is-danger');
    $('#input-nickname').focus();
    return;
  }
  if (!is_nickname2(nickname)) {
    $('#help-nick')
      .text('2~6자이상의 한글')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-nickname').focus();
    return;
  }

  $('#help-nick').addClass('is-loading');
  $.ajax({
    type: 'POST',
    url: '/sign_up/check_nick',
    data: {
      nickname_give: nickname,
    },
    success: function (response) {
      if (response['exists1']) {
        $('#help-nick')
          .text('이미 존재하는 닉네임입니다.')
          .removeClass('is-safe')
          .addClass('is-danger');
        $('#input-nickname').focus();
      } else {
        $('#help-nick')
          .text('사용가능 닉네임입니다.')
          .removeClass('is-danger')
          .addClass('is-success');
      }
      $('#help-nick').removeClass('is-loading');
    },
  });
}

// 회원가입 요청
function sign_up() {
  let username = $('#input-username').val();
  let nickname = $('#input-nickname').val();
  let introduce = $('#input-introduce').val();
  let password = $('#input-password').val();
  let password2 = $('#input-password2').val();

  if ($('#help-id').hasClass('is-danger')) {
    alert('5~20자 이상의 한글/영문/숫자');
    return;
  } else if (!$('#help-id').hasClass('is-success')) {
    alert('아이디 중복확인을 해주세요.');
    return;
  }

  if ($('#help-nick').hasClass('is-danger')) {
    alert('2~6자 이상의 한글');
    return;
  } else if (!$('#help-nick').hasClass('is-success')) {
    alert('닉네임 중복확인을 해주세요.');
    return;
  }

  if (password == '') {
    $('#help-password')
      .text('비밀번호를 입력해주세요.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password').focus();
    return;
  } else if (!is_password(password)) {
    $('#help-password')
      .text(
        '8~20자 이상의 한글/영문/숫자 포함 가능'
      )
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password').focus();
    return;
  } else {
    $('#help-password')
      .text('사용가능 비밀번호입니다.')
      .removeClass('is-danger')
      .addClass('is-success');
  }
  if (password2 == '') {
    $('#help-password2')
      .text('비밀번호를 입력해주세요.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password2').focus();
    return;
  } else if (password2 != password) {
    $('#help-password2')
      .text('비밀번호가 일치하지 않습니다.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password2').focus();
    return;
  } else {
    $('#help-password2')
      .text('')
      .removeClass('is-danger')
      .addClass('is-success');
  }
  $.ajax({
    type: 'POST',
    url: '/sign_up/save',
    data: {
      username_give: username,
      password_give: password,
      nickname_give: nickname,
      introduce_give: introduce,
    },
    success: function (response) {
      alert('득근하세요.');
      window.location.replace('/login');
    },
  });
}

function sign_in() {
  let username = $('#input-username').val();
  let password = $('#input-password').val();

  if (username == '') {
    $('#help-id-login').text('아이디를 입력해주세요.');
    $('#input-username').focus();
    return;
  } else {
    $('#help-id-login').text('');
  }

  if (password == '') {
    $('#help-password-login').text('비밀번호를 입력해주세요.');
    $('#input-password').focus();
    return;
  } else {
    $('#help-password-login').text('');
  }

  $.ajax({
    type: 'POST',
    url: '/sign_in',
    data: {
      username_give: username,
      password_give: password,
    },
    success: function (response) {
      if (response['result'] == 'success') {
        $.cookie('mytoken', response['token'], { path: '/' });
        window.location.replace('/');
      } else {
        alert(response['msg']);
      }
    },
  });
}

function time2str(date) {
  let today = new Date()
  let time = (today - date) / 1000 / 60  // 분

  if (time < 60) {
    return parseInt(time) + "분 전"
  }
  time = time / 60  // 시간
  if (time < 24) {
    return parseInt(time) + "시간 전"
  }
  time = time / 24
  if (time < 7) {
    return parseInt(time) + "일 전"
  }
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}
