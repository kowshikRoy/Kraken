Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;
function LoadTable(modelName, queryType, page=1, beginDate = null, endDate = null,
 product=null, client = null, region=null, salesman=null) {
 $.ajax({
  method 	:"GET",
  url		:'/api/' + modelName,
  data        : {
   'beginDate' : beginDate,
   'endDate'   : endDate,
   'queryType' : queryType,
   'page'      : page,
   'product'   : product,
   'client'    : client,
   'region'    : region,
   'salesman'  : salesman,
 },
 success: function(data){
   console.log(data);
   $('#' + modelName + "-"+ queryType + "-table").html(data.table)
   $('#' + modelName + "-"+ queryType + "-paginator").html(data.paginator)
 } ,
});
}

function LoadChart(modelName, beginDate = null, endDate = null,
 product=null, client = null, region=null, salesman=null) {
 $.ajax({
  method  :"GET",
  url   :'/api/chart/',
  data        : {
    'modelName': modelName,
   'beginDate' : beginDate,
   'endDate'   : endDate,
   'product'   : product,
   'client'    : client,
   'region'    : region,
   'salesman'  : salesman,
 },
 success: function(data){
  console.log(data);
   drawChart(document.getElementById("chart-"+ modelName), 'line', data,"Volume","Amount");
 } ,
});
}

function LoadDefault(modelName, queryType, page = 1) {
 $.ajax({
  method  :"GET",
  url   :'/api/default/',
  data        : {
   'modelName' : modelName,
   'queryType' : queryType,
   'page'      : page,
 },
 success: function(data){
   console.log(data);
   $('#' + modelName + "-"+ queryType + "-table").html(data.table)
   // $('#' + modelName + "-"+ "tk" + "-table").html(data.tk)
   $('#' + modelName + "-"+ queryType + "-paginator").html(data.paginator)
   // $('#' + modelName + "-"+ "tk" + "-paginator").html(data.tkPaginator)
   
 } ,
});
}



function drawChart(ctx, type, data, l1 = 'Product in volume',
  l2 = 'Product in amount'){
console.log(ctx);

 new Chart(ctx,
 {
  type: type,
  data: {
   labels: data['label'],
   datasets: [
   {
    label: l1,
    data: data['volume'],
    
    yAxisID: 'A',
    backgroundColor: 'rgba(3, 169, 244, 0.7)',

  },
  {
    label: l2,
    data: data['tk'],
    
    yAxisID: 'B',
    backgroundColor: 'rgba(156, 39, 176, 0.7)',
    
  }
  ],
},
options: {
    elements: {
            
            line: {
                tension: 0, // disables bezier curves
            }
        },
 scales: {
  yAxes: [{
    ticks: {
                beginAtZero: true
            },
   id: 'A',
   type: 'linear',
   position: 'left',
   scaleLabel: {
    display: true,
    labelString: 'Volume (quantity)'
  }

}, {
  ticks: {
                beginAtZero: true
            },
  id: 'B',
  scaleLabel: {
   display: true,
   labelString: 'Amount (Tk)'
 },

 type: 'linear',
 position: 'right',

 gridLines: {
   display:false
 }

}],
xAxes: [{
  barPercentage: .95,
  categoryPercentage: 0.6,
  gridLines: {
    display:false
  },
  scaleLabel: {
    display:true,
    labelString: 'Timeline'
  }
}],
}
}

}
);
}

function drawChartWithPrediction(ctx, type, data, l1 = 'Product in volume', l2 = 'Product in amount', l3 = 'Prediction in volume') {
    console.log(ctx);
    new Chart(
        ctx,
        {
            type: type,
            data: {
                labels: data['label'],
                datasets: [
                    {
                        label: l1,
                        data: data['volume'],
                        yAxisID: 'A',
                        backgroundColor: 'rgba(3, 169, 244, 0.7)',
                    },
                    {
                        label: l2,
                        data: data['tk'],
                        yAxisID: 'B',
                        backgroundColor: 'rgba(156, 39, 176, 0.7)',
                    },
                    {
                        label: l3,
                        data: data['prediction'],
                        yAxisID: 'A',
                        backgroundColor: 'rgba(3, 169, 244, 0.3)',
                    }
                ],
            },
            options: {
                elements: {
                    line: {
                        tension: 0, // disables bezier curves
                    }
                },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true
                            },
                            id: 'A',
                            type: 'linear',
                            position: 'left',
                            scaleLabel: {
                                display: true,
                                labelString: 'Volume (quantity)'
                            }
                        },
                        {
                            ticks: {
                                beginAtZero: true
                            },
                            id: 'B',
                            scaleLabel: {
                                display: true,
                                labelString: 'Amount (Tk)'
                            },
                            type: 'linear',
                            position: 'right',
                            gridLines: {
                                display:false
                            }
                        }
                    ],
                    xAxes: [
                        {
                            barPercentage: .95,
                            categoryPercentage: 0.6,
                            gridLines: {
                                display:false
                            },
                            scaleLabel: {
                                display:true,
                                labelString: 'Timeline'
                            }
                        }
                    ],
                }
            }
        }
    );
}

function drawOneChart(ctx, type, data){

 new Chart(ctx,
 {
  type: type,
  data: {
   labels: data['label'],
   datasets: [
   {
    label: 'Volume',
    data: data['data'],
    backgroundColor: palette('tol-rainbow', data['data'].length).map(function(hex) {return '#' + hex;}),

  },

  ],
},
options: {
 scales: {
  yAxes: [{
   ticks: {
    beginAtZero: true
  }
}],
xAxes: [{
  barPercentage: .95,
  categoryPercentage: 0.6,
  gridLines: {
   display:false
 }
}],
}
}

}
);
}

function LoadPrediction(modelName, queryId) {
 $.ajax({
  method      :"GET",
  url         :'/api/predict/' +  modelName,
  data        : {
   'model'   : modelName,
   'id'      : queryId,
 },
 success: function(data){
   drawOneChart(document.getElementById('prediction-'+modelName),'line', data)
 } ,
});
}

function LoadPercentlie(modelName) {
    $.ajax({
      method      :"GET",
      url         :'/api/percentile/',
      data        : {
        'modelName' : modelName.toUpperCase()
      },
      success: function(data){
        drawOneChart(document.getElementById('percentile-'+modelName),'bar', data)
      } ,
    });
  }


  