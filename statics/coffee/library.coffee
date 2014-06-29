jQuery ->
    window.starLibrary = (library_id) ->
        ret = $.ajax
            type: 'get'
            url: '/library/'+library_id+'/star/'
            success: (retData) ->
                if retData == '-1'
                    alert '에러가 발생했습니다!' 
                else
                    bt = $('.btn-star > span.glyphicon')
                    sc = $('.star-count')
                    sc_val = parseInt sc.text()
                    if retData == 'star'
                        sc.text (sc_val + 1)
                        bt.removeClass "glyphicon-star-empty"
                        bt.addClass "glyphicon-star"
                    else if retData == 'unstar'
                        sc.text (sc_val - 1)
                        bt.removeClass "glyphicon-star"
                        bt.addClass "glyphicon-star-empty"

            fail: ->
                alert '에러가 발생했습니다!'

    $(document).ready ->
        #
