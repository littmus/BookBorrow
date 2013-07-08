jQuery ->
    $(document).ready ->
        rating_input = $('input[name="review_star"]')
        $('#review_star').raty
            click: (score, evt) ->
                rating_input.val score

        $('button.btn-submit').click ->
            ret = $.ajax
                type: 'post'
                url: '/review/review_write_ok/'
                data: {
                    'book_id': BOOK_ID,
                    'rating': rating_input.val(),
                    'body': $('textarea[name="review_body"]').val(),
                }
                success: (retData) ->
                    if retData == "-1"
                        alert '에러가 발생했습니다!'
                    else
                        alert '리뷰가 저장되었습니다!'
                        $('#review').modal 'hide'
                        window.location.reload()
                fail: ->
                    alert '에러가 발생했습니다!'


        $('.review_star').each ->
            $(this).raty
                score: ->
                    return $(this).attr 'data-score'
                readOnly: true