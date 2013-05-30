jQuery ->
    window.starLibrary = (library_id) ->
        ret = $.ajax
            type: 'get'
            url: '/library/'+library_id+'/star/'
            success: (retData) ->
                if retData == '-1'
                    alert '에러가 발생했습니다!' 
                else
                    star = '<i class="icon-white icon-star"></i>'
                    star_empty = '<i class="icon-white icon-star-empty"></i>'
                    bt = $('.btn-star')
                    sc = $('.star-count')
                    sc_val = parseInt sc.text()
                    if retData == 'star'
                        sc.text (sc_val + 1)
                        bt.html(star)
                    else if retData == 'unstar'
                        sc.text (sc_val - 1)
                        bt.html(star_empty)

            fail: ->
                alert '에러가 발생했습니다!'

    $(document).ready ->
        #