function getImageUrl() {
  console.log('entered getImageUrl');
  return `https://i.ytimg.com/vi/${slicing_url}/sddefault.jpg`;
}

function isEmptyComment(content) {
  if (content === '') {
    return 1;
  }
  return 0;
}
function modifyComment(i, j, section, username) {
  let title = $(`#title-tag${i}`).text(); // 고유번호

  let content = $(`#edit-input-box${i}${j}`).val();
  if (isEmptyComment(content)) {
    alert('댓글을 입력해주세요~');
    $(`#edit-input-box${i}${j}`).focus();
    return;
  }

  let form_data = new FormData();
  form_data.append('section_give', section.toString());
  form_data.append('title_give', title);
  form_data.append('idx_give', j);
  form_data.append('content_give', content);

  $.ajax({
    type: 'POST',
    url: `/detail_page/${username}}/modify_comment`,
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert('modified comment!');
      window.location.reload();
    },
  });
}

// comment 수정하지 않고 취소하기
function cancelComment(i, j, section) {
  //input태그를 다시 span태그로 돌려놓기
  $(`#edit-input-box${i}${j}`)
    .contents()
    .unwrap()
    .wrap(`<p id="comment-tag${i}${j}"></p>`);

  //confirm 버튼을 delete 버튼으로 변경
  $(`#confirm-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<a  href="javascript:;" id="delete-btn${i}${j}" onclick="deleteComment(${i}, ${j}, '${section}')" class="a-tag-design"></a>`
    );
  $(`#delete-btn${i}${j}`).text('delete');

  //back-btn을 edit-btn으로 변경
  $(`#back-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<a id="edit-btn${i}${j}" href="javascript:;" onclick="editComment(${i}, ${j}, '${section}')" class="a-tag-design"></a>`
    );
  $(`#edit-btn${i}${j}`).text('edit');
}

function editComment(i, j, section, username) {
  // 편집 전 댓글 저장해둠.
  const before_comment = $(`#comment-tag${i}${j}`).text();

  // input창으로 변경
  $(`#comment-tag${i}${j}`)
    .contents()
    .unwrap()
    .wrap(`<input id="edit-input-box${i}${j}" value="${before_comment}"/>`);
  $(`#edit-input-box${i}${j}`).focus();

  // delete-btn => confirm-btn
  $(`#delete-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<a id="confirm-btn${i}${j}" href="javascript:;" class="a-tag-design" onclick="modifyComment(${i}, ${j}, '${section}', '${username}')"></a>`
    );
  $(`#confirm-btn${i}${j}`).text('confirm');

  // edit-btn => back-btn
  $(`#edit-btn${i}${j}`)
    .contents()
    .unwrap()
    .wrap(
      `<a id="back-btn${i}${j}" href="javascript:;" onclick="cancelComment(${i},${j}, '${section}')" class="a-tag-design"></a>`
    );
  $(`#back-btn${i}${j}`).text('back');
}
//
function addComment(idx, section, username) {
  let comment = $(`#comment${idx}`).val();
  let title = $(`#title-tag${idx}`).text(); // 식별자

  if (isEmptyComment(comment)) {
    alert('내용을 입력해주세요~');
    $(`#comment${idx}`).focus();
    return;
  }
  let form_data = new FormData();
  form_data.append('section_give', `${section}`);
  form_data.append('title_give', title);
  form_data.append('comment_give', comment);

  $.ajax({
    type: 'POST',
    url: `/detail_page/${username}/add_comment`,
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
function deleteComment(i, j, section) {
  let title = $(`#title-tag${i}`).text();

  let form_data = new FormData();
  form_data.append('section_give', section);
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
