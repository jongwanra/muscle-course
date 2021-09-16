function post() {
  let comment = $('#textarea-post').val();
  let today = new Date().toISOString();
  $.ajax({
    type: 'POST',
    url: '/posting',
    data: {
      comment_give: comment,
      date_give: today,
    },
    success: function (response) {
      $('#modal-post').removeClass('is-active');
      window.location.reload();
    },
  });
}

function time2str(date) {
  let today = new Date();
  let time = (today - date) / 1000 / 60; // 분

  if (time < 60) {
    return parseInt(time) + '분 전';
  }
  time = time / 60; // 시간
  if (time < 24) {
    return parseInt(time) + '시간 전';
  }
  time = time / 24;
  if (time < 7) {
    return parseInt(time) + '일 전';
  }
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
}

function get_posts() {
  $('#post-box').empty();
  $.ajax({
    type: 'GET',
    url: '/get_posts',
    data: {},
    success: function (response) {
      if (response['result'] == 'success') {
        let posts = response['posts'];
        for (let i = 0; i < posts.length; i++) {
          let post = posts[i];
          let time_post = new Date(post['date']);
          let time_before = time2str(time_post);
          let html_temp = `
          <div class="box" id="${post['_id']}">
            <article class="media">
                      <div class="media-left">
                          <a class="image is-64x64" href="/user/${post['username']}">
                              <img class="is-rounded" src="/static/${post['profile_pic_real']}"
                                    alt="Image">
                          </a>
                      </div>
                      <div class="media-content">
                          <div class="content">
                              <p>
                                  <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                  <br>
                                  ${post['comment']}
                              </p>
                          </div>
                      </div>
                  </article>
              </div>`;
          $('#post-box').append(html_temp);
        }
      }
    },
  });
}

$(document).ready(function () {
  get_posts();
});

function sign_out() {
  $.removeCookie('mytoken', { path: '/' });
  alert('로그아웃!');
  window.location.href = '/login';
}

function update_profile() {
  let name = $('#input-name').val();
  let file = $('#input-pic')[0].files[0];
  let about = $('#textarea-about').val();
  let form_data = new FormData();
  form_data.append('file_give', file);
  form_data.append('name_give', name);
  form_data.append('about_give', about);
  console.log(name, file, about, form_data);

  $.ajax({
    type: 'POST',
    url: '/update_profile',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response['result'] == 'success') {
        alert(response['msg']);
        window.location.reload();
      }
    },
  });
}

document.getElementById('btns-me').style.color = 'red';
document.getElementById('join').style.color = 'red';