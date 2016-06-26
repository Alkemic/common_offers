$(document).ready(function() {
    var loading = $("#loading");

    $("#ceneo-form").submit(function(e) {
        e.preventDefault();
        var self = $(this);
        var resultsUl = $('#ceneo-results');
        resultsUl.empty().hide();
        loading.show();

        $.post('/ceneo', self.serialize(), function(data){
            loading.hide();
            resultsUl.show();
            console.log(data.result);
            data.result.forEach(function(row) {
                products = [];
                row.products.forEach(function(product) {
                    products.push(product.name + ' ' + product.price.toFixed(2));
                });
                $('<li><b>' + row.shop + ' ' + row.price.toFixed(2) + ' ' + row.products.length + ' prod.</b> (' + products.join(', ') + ')</li>').appendTo(resultsUl);
            });
        }).fail(function(data){
            loading.hide();
            resultsUl.show();
            $('<li class="error">Error occured!</li>').appendTo(resultsUl);
        });
    });

    $("#allegro-form").submit(function(e) {
        e.preventDefault();
        var self = $(this);
        var resultsUl = $('#allegro-results');
        resultsUl.empty().hide();
        loading.show();

        $.post('/allegro', self.serialize(), function(data){
            loading.hide();
            resultsUl.show();
            console.log(data.result);
            data.result.forEach(function(row) {
                products = [];
                row.products.forEach(function(product) {
                    products.push(product.name + ' ' + product.price.toFixed(2));
                });
                $('<li><b>' + row.shop + ' ' + row.price.toFixed(2) + ' ' + row.products.length + ' prod.</b> (' + products.join(', ') + ')</li>').appendTo(resultsUl);
            });
        }).fail(function(data){
            loading.hide();
            resultsUl.show();
            $('<li class="error">Error occured!</li>').appendTo(resultsUl);
        });
    });
});