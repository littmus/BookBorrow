/**
 * Pinry
 * Descrip: Core of pinry, loads and tiles pins.
 * Authors: Pinry Contributors
 * Updated: Apr 5th, 2013
 * Require: jQuery, Pinry JavaScript Helpers
 */


$(window).load(function() {
    /**
     * tileLayout will simply tile/retile the block/pin container when run. This
     * was put into a function in order to adjust frequently on screen size 
     * changes.
     */
    window.tileLayout = function() {
        var blockContainer = $('#books'),
            blocks = blockContainer.children('.book'),
            blockMargin = 15,
            blockWidth = 218,
            rowSize = Math.floor(blockContainer.width()/(blockWidth+blockMargin)),
            colHeights = [],
            rowMargins = [],
            marginLeft = 0;

        // Fill our colHeights array with 0 for each row we have
        for (var i=0; i < rowSize; i++) colHeights[i] = 0;
        // Fill out our rowMargins which will be static after this
        for (var i=0; i < rowSize; i++) {
            // Our first item has a special margin to keep things centered
            if (i == 0) rowMargins[0] = (blockContainer.width()-rowSize*(blockWidth+blockMargin))/2;
            else rowMargins[i] = rowMargins[i-1]+(blockWidth+blockMargin);
        }
        // Loop through every block
        for (var b=0; b < blocks.length; b++) {
            // Get the jQuery object of the current block
            block = blocks.eq(b);
            // Position our new pin in the shortest column
            var sCol = 0;
            for (var i=0; i < rowSize; i++) {
                if (colHeights[sCol] > colHeights[i]) sCol = i;
            }
            block.css({
                'margin-left': rowMargins[sCol],
                'margin-top':  colHeights[sCol],
            });

            text = block.children('.text')
            text_top = block.height() - text.height() - 10
            text.css({
                'top': text_top,
            })

            block.fadeIn(300);
            colHeights[sCol] += block.height()+(blockMargin);

        }

        $('.book').each(function() {
            var book = $(this);
            book.off('hover')
            book.hover(function() {
                book.children('.text').stop(true, true).fadeIn(300);
            }, function() {
                book.children('.text').stop(true, false).fadeOut(300);
            });

        });

        $('.spinner').css('display', 'none');
        blockContainer.css('height', colHeights.sort().slice(-1)[0]);
    }

    /**
     * On scroll load more pins from the server
     */
    window.scrollHandler = function() {
        var windowPosition = $(window).scrollTop() + $(window).height();
        var bottom = $(document).height() - 100;
        if(windowPosition > bottom) loadPins();
    }

    /**
     * Load our pins using the pins template into our UI, be sure to define a
     * offset outside the function to keep a running tally of your location.
     */
    function loadPins() {
        // Disable scroll
        $(window).off('scroll');

        // Show our loading symbol
        $('.spinner').css('display', 'block');

        // Fetch our pins from the api using our current offset
        var apiUrl = '/api/android/book/?offset='+String(offset);
        apiUrl += '&library_id=' + libraryId;
        $.get(apiUrl, function(books) {
            // Set which items are editable by the current user
            //for (var i=0; i < books.objects.length; i++)
            //    books.objects[i].editable = (books.objects[i].submitter.username == currentUser.username);

            // Use the fetched pins as our context for our pins template
            var template = Handlebars.compile($('#books-template').html());
            var html = template({books: books.objects});

            // Append the newly compiled data to our container
            $('#books').append(html);

            // We need to then wait for images to load in and then tile
            $('#books img').load(function() {
                $(this).fadeIn(300);
                tileLayout();
            });

            var empty_msg = "<div class='span12'><div class='alert alert-error alert-block'>등록된 책이 없습니다!</div></div>";
            if (books.objects.length == 0) {
                $('#books').prepend(empty_msg);
            }

            if (books.objects.length < apiLimitPerPage) {
                $('.spinner').css('display', 'none');
            }
            else {
                $(window).scroll(scrollHandler);
            }
        });

        // Up our offset, it's currently defined as 50 in our settings
        offset += apiLimitPerPage;
        //setTimeout($(window).trigger('resize'), 1000)
        //tileLayout();
    }


    // Set offset for loadPins and do our initial load
    var offset = 0;
    loadPins();

    // If our window gets resized keep the tiles looking clean and in our window
    $(window).resize(function() {
        tileLayout();
    })
});
