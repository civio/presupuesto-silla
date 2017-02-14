// Theme custom js methods
$(document).ready(function(){

  // Add treemap alert
  var addChartsAlert = function() {
    var str = {
      chapter: {
        'es': 'Ingresos por capítulo',
        'ca': 'Ingressos per capítol'
      },
      article: {
        'es': 'Ingresos por artículo',
        'ca': 'Ingressos per article'
      },
    };

    $('.policies-chart #budget-summary').prepend('<div class="alert alert-incomes">'+str.chapter[ $('html').attr('lang') ]+'</div>');
    $('.policies-chart #budget-summary').append('<div class="alert alert-incomes">'+str.article[ $('html').attr('lang') ]+'</div>');
     
  };

  // show / hide treemap alert based on selected tab
  var setupChartsAlert = function(state) {
    if (state == 'income') {
      $('.policies-chart #budget-summary .alert-incomes').show();
    } else {
      $('.policies-chart #budget-summary .alert-incomes').hide();
    }
  };

  addChartsAlert();

  setupChartsAlert($('section').data('tab'));

  $(window).bind('hashchange', function(e) {
    var state = $.deparam.fragment();
    setupChartsAlert(state.view);
  });
});