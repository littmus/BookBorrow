jQuery ->
    $(document).ready ->
        $.datepicker.regional["ko"] =
            closeText: "닫기"
            prevText: "이전"
            nextText: "다음"
            currentText: "오늘"
            monthNames: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
            monthNamesShort: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
            dayNames: ["일", "월", "화", "수", "목", "금", "토"]
            dayNamesShort: ["일", "월", "화", "수", "목", "금", "토"]
            dayNamesMin: ["일", "월", "화", "수", "목", "금", "토"]
            weekHeader: "Wk"
            dateFormat: "yy-mm-dd"
            firstDay: 0
            isRTL: false
            showMonthAfterYear: true
            yearSuffix: ""

        $.datepicker.setDefaults $.datepicker.regional["ko"]

        start_date = $('input[name="start_date"]')
        return_date = $('input[name="return_date"]')

        start_date.datepicker()
        return_date.datepicker()

        today = new Date()
        today_val = $.datepicker.formatDate('yy-mm-dd', today)
        today = $.datepicker.parseDate('yy-mm-dd', today_val)
        
        start_date.change ->
            sd = $.datepicker.parseDate('yy-mm-dd', start_date.val())

            if sd < today
                console.log(sd)
                console.log(today)
                alert '시작일은 오늘 부터 가능합니다!'
                start_date.val('')

        return_date.change ->
            rd = $.datepicker.parseDate('yy-mm-dd', return_date.val())

            if rd < today
                alert '반납일은 내일 부터 가능합니다!'
                return_date.val('')

            if start_date.val() != ''
                sd = $.datepicker.parseDate('yy-mm-dd', start_date.val())

                if rd <= sd
                    alert '반납일이 대여일 이후로 가능합니다!'
                    return_date.val('')