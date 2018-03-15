Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;
function LoadTable(
  modelName,
  queryType,
  page = 1,
  beginDate = null,
  endDate = null,
  product = null,
  client = null,
  region = null,
  salesman = null
) {
    document.getElementById(modelName + "-" + queryType + "-table").innerHTML = "<h4>Loading please wait...</h4>";
      $.ajax({
        method: "GET",
        url: "/api/" + modelName,
        data: {
          beginDate: beginDate,
          endDate: endDate,
          queryType: queryType,
          page: page,
          product: product,
          client: client,
          region: region,
          salesman: salesman
        },
        success: function(data) {
          console.log(data);
          $("#" + modelName + "-" + queryType + "-table").html(data.table);
          $("#" + modelName + "-" + queryType + "-paginator").html(data.paginator);
        }
  });
}

function LoadChart(
  modelName,
  beginDate = null,
  endDate = null,
  product = null,
  client = null,
  region = null,
  salesman = null
) {
  $.ajax({
    method: "GET",
    url: "/api/chart/",
    data: {
      modelName: modelName,
      beginDate: beginDate,
      endDate: endDate,
      product: product,
      client: client,
      region: region,
      salesman: salesman
    },
    success: function(data) {
      console.log(data);
      document.getElementById("chart-" + modelName + "-area").innerHTML = '<canvas id="chart-' + modelName + '" height="120"></canvas>';
      drawChart(
        document.getElementById("chart-" + modelName),
        "line",
        data,
        "Volume",
        "Amount"
      );
    }
  });
}

function LoadDiscountImpact (
    modelName,
    product = null,
    client = null,
    region = null,
    salesman = null
) {
    document.getElementById("discount-" + modelName + "-area").innerHTML = "<h4>Loading please wait...</h4>";
    $.ajax({
        method: "GET",
        url: "/api/discount-impact/",
        data: {
            modelName: modelName,
            product: product,
            client: client,
            region: region,
            salesman: salesman
        },
        success: function(data) {
        console.log(data);
            document.getElementById("discount-" + modelName + "-area").innerHTML='<canvas id="discount-' + modelName + '" height="' + data["labels"].length*30 + '"></canvas>';
            drawDiscountGraph(
                document.getElementById("discount-" + modelName),
                "horizontalBar",
                data
            );
        }
    });
}

function LoadDefault(modelName, queryType, page = 1) {
  $.ajax({
    method: "GET",
    url: "/api/default/",
    data: {
      modelName: modelName,
      queryType: queryType,
      page: page
    },
    success: function(data) {
      console.log(data);
      $("#" + modelName + "-" + queryType + "-table").html(data.table);
      // $('#' + modelName + "-"+ "tk" + "-table").html(data.tk)
      $("#" + modelName + "-" + queryType + "-paginator").html(data.paginator);
      // $('#' + modelName + "-"+ "tk" + "-paginator").html(data.tkPaginator)
    }
  });
}

function drawDiscountGraph (ctx, type, data) {
    new Chart (ctx, {
        type: type,
        data: {
            labels: data["labels"],
            datasets: [
                {
                    label: 'Sales amount for 3 months before discount',
                    data: data["beforeAmounts"],
                    hidden:false,
                    backgroundColor: "rgba(3, 169, 244, 0.7)"
                },
                {
                    label: 'Sales amount for 3 months after discount',
                    data: data["afterAmounts"],
                    hidden:false,
                    backgroundColor: "rgba(156, 39, 176, 0.7)"
                }
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Amount (Tk)",
                        },
                    }
                ]
            }
        }
    });
}

function drawChart(
  ctx,
  type,
  data,
  l1 = "Product in volume",
  l2 = "Product in amount"
) {
  console.log(ctx);

  var secondChartYAxisID = "B";
  if (l2 == "Second") {
    secondChartYAxisID = "A";
  }
  new Chart(ctx, {
    type: type,
    data: {
      labels: data["label"],
      datasets: [
        {
          label: l1,
          data: data["volume"],
          hidden:false,

          yAxisID: "A",
          backgroundColor: "rgba(3, 169, 244, 0.7)"
        },
        {
          label: l2,
          data: data["tk"],
          hidden : false,

          yAxisID: secondChartYAxisID,
          backgroundColor: "rgba(156, 39, 176, 0.7)"
        }
      ]
    },
    options: {
      elements: {
        line: {
          tension: 0 // disables bezier curves
        }
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            },
            id: "A",
            type: "linear",
            position: "left",
            scaleLabel: {
              display: true,
              labelString: "Volume (quantity)",
              
            },
            afterFit: function(scaleInstance) {
                scaleInstance.width = 100; // sets the width to 100px
              }
          },
          {
            ticks: {
              beginAtZero: true
            },
            id: "B",
            display: (secondChartYAxisID == "B"),
            scaleLabel: {
              display: (secondChartYAxisID == "B"),
              labelString: "Amount (Tk)",
              
            },
            afterFit: function(scaleInstance) {
                scaleInstance.width = 100; // sets the width to 100px
              },

            type: "linear",
            position: "right",

            gridLines: {
              display: false,
            }
          }
        ],
        xAxes: [
          {
            barPercentage: 0.95,
            categoryPercentage: 0.6,
            gridLines: {
              display: false,
            },
            scaleLabel: {
              display: true,
              labelString: "Timeline"
            }
          }
        ]
      },
      legend: {
        onClick: function(evt, item) {
                var index = item.datasetIndex;
                
                var ch = $(this)[0].chart;

                if (secondChartYAxisID == "B") {
                    ch.options.scales.yAxes[index].display= !ch.options.scales.yAxes[index].display;
                }
                ch.data.datasets[index].hidden = !ch.data.datasets[index].hidden

                if(ch.data.datasets[0].hidden == false) {
                    ch.options.scales.yAxes[0].gridLines.display = true;
                    ch.options.scales.yAxes[1].gridLines.display = false;
                    
                }
                else if(ch.data.datasets[1].hidden == false) {
                    ch.options.scales.yAxes[0].gridLines.display = false;
                    ch.options.scales.yAxes[1].gridLines.display = true;
                   
                }
                

                ch.update();
                
            }
        },
    }
  });
}



function drawOneChart(ctx, modelName, type, data) {
  new Chart(ctx, {
    type: type,
    data: {
      labels: data["label"],
      datasets: [
        {
          label: "Percentile",
          data: data["data"],
          backgroundColor: palette("tol-rainbow", data["data"].length).map(
            function(hex) {
              return "#" + hex;
            }
          )
        }
      ]
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              max: 100
            },
            scaleLabel: {
                display: true,
                labelString: "Sales percentile in amount"
            }
          }
        ],
        xAxes: [
          {
            barPercentage: 0.95,
            categoryPercentage: 0.6,
            gridLines: {
              display: false
            },
            scaleLabel: {
                display: true,
                labelString: capitalizeFirstLetter(modelName) + " percentile"
            }
          }
        ]
      }
    }
  });
}

function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function LoadPrediction(modelName, queryId) {
  $.ajax({
    method: "GET",
    url: "/api/predict/" + modelName,
    data: {
      model: modelName,
      id: queryId
    },
    success: function(data) {
      drawOneChart(
        document.getElementById("prediction-" + modelName),
        modelName,
        "line",
        data
      );
    }
  });
}

function LoadPercentlie(modelName) {
  $.ajax({
    method: "GET",
    url: "/api/percentile/",
    data: {
      modelName: modelName.toUpperCase()
    },
    success: function(data) {
      drawOneChart(
        document.getElementById("percentile-" + modelName),
        modelName,
        "bar",
        data
      );
    }
  });
}
function drawChartWithPrediction(
    ctx,
    type,
    data,
    l1 = "Product in volume",
    l2 = "Product in amount",
    l3 = "Prediction in volume"
  ) {
    console.log(ctx);
    new Chart(ctx, {
      type: type,
      data: {
        labels: data["label"],
        datasets: [
          {
            label: l1,
            data: data["volume"],
            yAxisID: "A",
            backgroundColor: "rgba(3, 169, 244, 0.7)"
          },
          {
            label: l2,
            data: data["tk"],
            yAxisID: "B",
            backgroundColor: "rgba(156, 39, 176, 0.7)"
          },
          {
            label: l3,
            data: data["prediction"],
            yAxisID: "A",
            backgroundColor: "rgba(3, 169, 244, 0.3)"
          }
        ]
      },
      options: {
        elements: {
          line: {
            tension: 0 // disables bezier curves
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              id: "A",
              type: "linear",
              position: "left",
              scaleLabel: {
                display: true,
                labelString: "Volume (quantity)"
              },
              afterFit: function(scaleInstance) {
                  scaleInstance.width = 100; // sets the width to 100px
                }
            },
            {
              ticks: {
                beginAtZero: true
              },
              id: "B",
              scaleLabel: {
                display: true,
                labelString: "Amount (Tk)"
              },
              type: "linear",
              position: "right",
              gridLines: {
                display: false
              },
              afterFit: function(scaleInstance) {
                  scaleInstance.width = 100; // sets the width to 100px
                }
            },
            {
              ticks: {
                beginAtZero: true
              },
              id: "B",
              scaleLabel: {
                display: true,
                labelString: "Amount (Tk)"
              },
              type: "linear",
              position: "right",
              gridLines: {
                display: false
              },
              afterFit: function(scaleInstance) {
                  scaleInstance.width = 100; // sets the width to 100px
                }
            },
          ],
          xAxes: [
            {
              barPercentage: 0.95,
              categoryPercentage: 0.6,
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: "Timeline"
              }
            }
          ]
        },
        legend: {
          onClick: function(evt, item) {
                  var index = item.datasetIndex;
                  console.log(index);
                  
                  var ch = $(this)[0].chart;
                  // console.log(ch);
                  ch.options.scales.yAxes[index].display= !ch.options.scales.yAxes[index].display;
                  ch.data.datasets[index].hidden = !ch.data.datasets[index].hidden
                  console.log(ch.options.scales.yAxes[index].display);
  
                  ch.update();
                  
              }
          },
      }
    });
  }