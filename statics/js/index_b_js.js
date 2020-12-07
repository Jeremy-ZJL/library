// 删除书籍
$('.del_btn').click(function () {
    let $this = $(this);
    let books_pk = $this.attr('books_pk');
    // console.log(books_pk);
    $.ajax({
        url: '/del_book/',
        type: 'POST',
        data: {
            books_pk: books_pk,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (ret) {
            console.log(ret);
            if (ret.status) {
                $this.parent().parent().html("<td style='color:red;' colspan=7>删除成功！</td>");
            } else {
                alert(ret['msg']);
            }
        }
    })
});

// 新增-保存-模态框
$('#save_btn').click(function () {
    $('#myModal').modal('hide');
    let title = $('#book_title').val();
    let price = $('#book_price').val();
    let author = $('#book_author').val();
    let book_publish = $('#book_publish').val();
    // console.log(book_publish)
});
