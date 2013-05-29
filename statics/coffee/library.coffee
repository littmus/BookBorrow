jQuery ->
    window.starLibrary = (library_id) ->
            ret = $.ajax
                type: 'get'
                url: '/library/'+library_id+'/star/'
                success: (retData) ->
                    if retData == '-1'
                        alert '에러가 발생했습니다!'
                    #else if retData == '0'
                fail: ->
                    alert '에러가 발생했습니다!'

    $(document).ready ->
        #