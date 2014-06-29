jQuery ->
    $(document).ready ->
        $('input[name="isbn"]').popover(
            {
                'placement': 'bottom', 'trigger': 'focus', 'html': 'false',
                'content': '<img src="/static/img/isbn.png" style="width:100%;"><p style="text-align:center;">\'-\'를 제외하고 입력해 주세요</p>',
                'container': 'body'
            }
        )

        $('#isbn_check').click ->
            isbn = $('input[name="isbn"]').val()

            if isbn is ''
                alert 'ISBN을 입력해 주세요!'

            else
                if isbn.length != 10 and isbn.length != 13
                    alert '잘못된 ISBN 입니다!'
                else
                    ret = $.ajax
                        type: 'post'
                        url: '/book/isbn_search/'
                        data: {'isbn': isbn}
                        success: (retData) ->
                            if retData  == '-1'
                                alert '도서가 검색되지 않았습니다. 정보를 직접 입력해 주세요!'

                                $('input[name="title"]').val('').removeAttr 'disabled'
                                $('input[name="author"]').val('').removeAttr 'disabled'
                            else
                                $('input[name="title"]').val(retData.fields.title).attr 'disabled', 'disabled'
                                $('input[name="author"]').val(retData.fields.author).attr 'disabled', 'disabled'
                        fail: ->
                            alert '에러가 발생했습니다. 다시 한 번 검색해 보세요!'
