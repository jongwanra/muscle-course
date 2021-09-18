
function getImageUrl(slicing_url) {
  return `https://i.ytimg.com/vi/${slicing_url}/sddefault.jpg`;
}

function modifyComment(i, j) {
  let title = $(`#title-tag${i}`).text(); // 고유번호
  let content = $(`#edit-input-box${i}${j}`).val();

  let form_data = new FormData();
  form_data.append('section_give', '{{section}}');
  form_data.append('title_give', title);
  form_data.append('idx_give', j);
  form_data.append('content_give', content);

  $.ajax({
    type: 'POST',
    url: '/detail_page/{{user_info.username}}/modify_comment',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.reload();
    },
  });
}

// comment 수정하지 않고 취소하기
function cancelComment(i, j) {
  $(`#comment-username${i}${j}`).show();
  //input태그를 다시 span태그로 돌려놓기
  $(`#edit-input-box${i}${j}`)
    .contents()
    .unwrap()
    .wrap(`<span id="comment-tag${i}${j}"></span>`);

  //confirm 버튼을 delete 버튼으로 변경
  $(`#confirm-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<button id="delete-btn${i}${j}" onclick="deleteComment(${i}, ${j})" type="button" class="btn btn-link"></button>`
    );
  $(`#delete-btn${i}${j}`).text('delete');

  //back-btn을 edit-btn으로 변경
  $(`#back-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<button id="edit-btn${i}${j}" onclick="editComment(${i}, ${j})" type="button" class="btn btn-link"></button>`
    );
  $(`#edit-btn${i}${j}`).text('edit');
}

function editComment(i, j) {
  // 편집 전 댓글 저장해둠.
  const before_comment = $(`#comment-tag${i}${j}`).text();

  // input창으로 변경
  $(`#comment-tag${i}${j}`)
    .contents()
    .unwrap()
    .wrap(`<input id="edit-input-box${i}${j}" value="${before_comment}"/>`);
  $(`#comment-username${i}${j}`).hide();
  $(`#edit-input-box${i}${j}`).focus();

  // delete-btn => confirm-btn
  $(`#delete-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<button id="confirm-btn${i}${j}" onclick="modifyComment(${i}, ${j})" type="button" class="btn btn-link"></button>`
    );
  $(`#confirm-btn${i}${j}`).text('confirm');

  // edit-btn => back-btn
  $(`#edit-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<button id="back-btn${i}${j}" onclick="cancelComment(${i},${j})" type="button" class="btn btn-link"></button>`
    );
  $(`#back-btn${i}${j}`).text('back');
}
//
function addComment(idx) {
  let comment = $(`#comment${idx}`).val();
  let title = $(`#title-tag${idx}`).text();

  let form_data = new FormData();
  form_data.append('section_give', '{{section}}');
  form_data.append('title_give', title);
  form_data.append('comment_give', comment);

  $.ajax({
    type: 'POST',
    url: '/detail_page/{{user_info.username}}/add_comment',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.reload();
    },
  });
}
// delete Comment Function
function deleteComment(i, j) {
  let title = $(`#title-tag${i}`).text();

  let form_data = new FormData();
  form_data.append('section_give', '{{section}}');
  form_data.append('title_give', title);
  form_data.append('idx_give', j);

  $.ajax({
    type: 'POST',
    url: '/detail_page/{{user_info.username}}/delete_comment',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.reload();
    },
  });
}
