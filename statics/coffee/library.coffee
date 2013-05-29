jQuery ->
    $(document).ready ->
        starLibrary = (library_id) ->
            ret = $.ajax
                type: 'post'
                url: '/library/'+library_id+'/star/'
                success: (retData) ->
                    if retData == '-1'
                        alert '에러가 발생했습니다!'
                    #else if retData == '0'



