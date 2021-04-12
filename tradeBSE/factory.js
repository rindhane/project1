var app = angular.module('myapp', ["appglobal", "topHeader"]);
var mydata;
app.config(function ($provide, $sceDelegateProvider) {
    //$sceProvider.enabled(false);
 $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from outer templates domain.
    'https://beta.bseindia.com/**'
  ]); 

    $provide.decorator('$exceptionHandler', function ($delegate) {
        return function (exception, cause) {
            $delegate(exception, cause);
            try{
                console.log('Error occurred! '+exception);
            }
            catch(err)
            {
                console.log(err);
            }
        };
    });
});
app.value('$', $);

app.factory('stockTickerData', ['$', '$rootScope', '$http', '$timeout', function ($, $rootScope, $http, $timeout) {
    $rootScope.isEquity = true;
    $rootScope.isDerivatie = false
    $rootScope.isCurrency = false;
    function stockTickerOperations() {
        var setValues;
        var updateStocks;
        var getSenValContr;
        var arrScripCode = new Array();
        $rootScope.socket;
		
        var setCallbacks = function (setValuesCallback, updateStocksCallback, getSenVal) {
            setValues = setValuesCallback;
            updateStocks = updateStocksCallback;
            getSenValContr = getSenVal;
          
        };
        
        //for  table sorter//
        $rootScope.propertyName = 'TurnOver';// null;//
        $rootScope.reverse = true;
        $rootScope.sortBy = function (propertyName) {
            $rootScope.reverse = ($rootScope.propertyName === propertyName) ? !$rootScope.reverse : false;
            $rootScope.propertyName = propertyName;
        };

        try {

            try {//https://streamlive.bseindia.com

                $rootScope.socket = io.connect("https://streamlive.bseindia.com", { upgrade: true, 'transports': ['websocket'] });

                $rootScope.socket.on('reconnect', function (attemptNumber) {
                    //console.log("reconnect.....")
                });

                $rootScope.socket.on('error', function (err) {
                    console.log("err......", err)
                })

                $rootScope.socket.on('connect_error', function (error) {
                    console.log("ecerrr", error)
                });

                $rootScope.socket.on('reconnecting', function (attemptNumber) {
                    //console.log("on reconnecting", attemptNumber)
                });

                $rootScope.socket.on('disconnect', function () {
                    console.log("disconnected......");
                })

                $rootScope.socket.on('connect', function () {
                    console.log("Connected");

               // $rootScope.socket.emit('joinChannel', { channel: "EQ30SCWeb" });
                    if ($rootScope.btnVl == 1) {

                        $rootScope.socket.emit('joinChannel', { channel: "SenSexValue" });
                        var grp = $('#dllUAssetgrp option:selected').val();

                        if (grp == "Equity") {
                            $rootScope.socket.emit('joinChannel', { channel: "EQ30SCWeb" });
                        } else if (grp == "Currency") {
                            $rootScope.socket.emit('joinChannel', { channel: "CU" });
                        } else if (grp == "Derivatives") {
                            $rootScope.socket.emit('joinChannel', { channel: "DR" });
                        }
                        else if (grp == "COMM") {
                            $rootScope.socket.emit('joinChannel', { channel: "COMM" });
                        }
                        $rootScope.socket.emit('joinChannel', { channel: "EQ30SCWeb" });
                    }
                });



                $rootScope.socket.on("Sensex", function (data) {
                
                    var data1 = JSON.parse(data)
                    var date = new Date();
                    var hh = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                    var mm = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();

                    if ((9 <= hh) && (hh <= 15)) {
                        //console.log("(hh) >= 15");
                        if ((hh) == 15) {
                            if ((mm) < 31) {
                                //console.log("hh is 3 but mm is < 31");
                                $('#id01').text(data1.IndexValue);
                                if (parseFloat(data1.percChange) < 0) {
                                    $('#id01').addClass('sengreencssIndx');
                                    $('#id02').addClass('sengreencssIndx');
                                    $('#id02').text(data1.percChange);

                                    $('#id01').removeClass('senredcssIndx');
                                    $('#id02').removeClass('senredcssIndx');
                                }
                                else {
                                    $('#id01').addClass('senredcssIndx');
                                    $('#id02').addClass('senredcssIndx');
                                    $('#id02').text("+" + data1.percChange);
                                    $('#id01').removeClass('sengreencssIndx');
                                    $('#id02').removeClass('sengreencssIndx');
                                }
                            }
                            else {
                                //console.log("take value from db");
                                $timeout(function () {
                                    $rootScope.$apply(getSenValContr());
                                }, 2000);
                            }
                        }
                        else {
                            $('#id01').text(data1.IndexValue);
                            if (parseFloat(data1.percChange) < 0) {
                                $('#id01').addClass('sengreencssIndx');
                                $('#id02').addClass('sengreencssIndx');
                                $('#id02').text(data1.percChange);
                                $('#id01').removeClass('senredcssIndx');
                                $('#id02').removeClass('senredcssIndx');
                            }
                            else {
                                $('#id01').addClass('senredcssIndx');
                                $('#id02').addClass('senredcssIndx');
                                $('#id02').text("+" + data1.percChange);
                                $('#id01').removeClass('sengreencssIndx');
                                $('#id02').removeClass('sengreencssIndx');
                            }
                        }
                    }
                    else {
                        
                        $timeout(function () {
                            $rootScope.$apply(getSenValContr());
                        }, 2000);
                    }
                })

                $rootScope.socket.on("Equity30SCW", function (data) {
                   
                    var jsonObj = [];
                    var arrData = data.split('|');
                    item = {};
                    var arrProp = ["Symbol", "Flag", "MsgType", "SessionNumber", "IndicativePrice", "IndicativeQty", "PercentChange", "NoOfTrades", "LastTradeQty", "TradeValFlag", "PreCloseRate", "Price", "Volume", "BuyPrice", "BuyPrice2", "BuyPrice3", "BuyPrice4", "BuyPrice5", "SellPrice", "SellPrice2", "SellPrice3", "SellPrice4", "SellPrice5", "BuyQty", "BuyQty2", "BuyQty3", "BuyQty4", "BuyQty5", "SellQty", "SellQty2", "SellQty3", "SellQty4", "SellQty5", "Bids1", "Bids2", "Bids3", "Bids4", "Bids5", "Ask1", "Ask2", "Ask3", "Ask4", "Ask5", "TurnOver"];
                    for (var i = 0; i < arrProp.length; i++) {
                        //  jsonObj[arrProp[i]] = arrNewData[i];
                        item[arrProp[i]] = arrData[i];
                    }
                    jsonObj.push(item);
                    //var eqData = eval("[" + jsonObj[0] + "]");
                    var eqData =   jsonObj[0]  ; //console.log("EQ.........", eqData)
                    $rootScope.SessionNo = eqData.SessionNumber;
                    $rootScope.$apply(updateStocks(eqData));
                })

                $rootScope.socket.on("CU", function (data) {
                    //console.log("CU.........")
                    $rootScope.$apply(updateStocks(JSON.parse(data)));
                })

                $rootScope.socket.on("DR", function (data) {
                    //console.log("DR.........")
                    $rootScope.$apply(updateStocks(JSON.parse(data)));
                })
                $rootScope.socket.on("COMM", function (data) {
                    //console.log("COMM.........")
                    $rootScope.$apply(updateStocks(JSON.parse(data)));
                })
            }
            catch(e)
            {
                console.log(e);
            }
            


            var FactDropDownChnaged = function (grp, ddlVal2, ddlVal3, sc) {
                try
                {
                    //console.log("....",grp,ddlVal2,ddlVal3)
                    $rootScope.socket.emit('joinChannel', { channel: "SenSexValue" });
                    if (grp == "Equity" && ddlVal2 == "Index" && ddlVal3 == "S&P BSE SENSEX") {

                        $rootScope.socket.emit('joinChannel', { channel: "EQ30SCWeb" });
                        $rootScope.socket.emit('leaveChannel', { channel: "CU" });
                        $rootScope.socket.emit('leaveChannel', { channel: "DR" });
                        $rootScope.socket.emit('leaveChannel', { channel: "COMM" });
                    }
                    else if (grp == "Currency" && ddlVal2 == "All" && ddlVal3 == "All") {

                        $rootScope.socket.emit('joinChannel', { channel: "CU" });
                        $rootScope.socket.emit('leaveChannel', { channel: "EQ30SCWeb" });
                        $rootScope.socket.emit('leaveChannel', { channel: "DR" });
                        $rootScope.socket.emit('leaveChannel', { channel: "COMM" });
                    }
                    else if (grp == "Derivatives" && ddlVal2 == "All" && ddlVal3 == "All") {

                        $rootScope.socket.emit('joinChannel', { channel: "DR" });
                        $rootScope.socket.emit('leaveChannel', { channel: "CU" });
                        $rootScope.socket.emit('leaveChannel', { channel: "EQ30SCWeb" });
                        $rootScope.socket.emit('leaveChannel', { channel: "COMM" });
                    }
                    else if (grp == "COMM" && ddlVal2 == "All" && ddlVal3 == "All") {

                        $rootScope.socket.emit('joinChannel', { channel: "COMM" });
                        $rootScope.socket.emit('leaveChannel', { channel: "CU" });
                        $rootScope.socket.emit('leaveChannel', { channel: "DR" });
                        $rootScope.socket.emit('leaveChannel', { channel: "EQ30SCWeb" });
                    }
                    else {
                        console.log("match not found");
                        $rootScope.socket.emit('leaveChannel', { channel: "CU" });
                        $rootScope.socket.emit('leaveChannel', { channel: "EQ" });
                        $rootScope.socket.emit('leaveChannel', { channel: "DR" });
                        $rootScope.socket.emit('leaveChannel', { channel: "COMM" });
                    }
                }
                catch (e) {
                    console.log(e);
                }
               
            };
            var graphEq= function (data, sc) {
                if (sc != null && sc != "") {
                    try {
                        var chartdivLabel = "div" + sc;
                        //$('#div' + sc).removeClass('loadGraphCss');
                        //$('#div' + sc).removeClass('loader');
                        chart = AmCharts.makeChart(chartdivLabel, {
                            "type": "stock",
                            "theme": "light",
                            "categoryAxesSettings": {
                                //"maxSeries": 10,
                                "minPeriod": "mm",
                                "groupToPeriods": ['mm'], //['mm', 'ss'],
                                "equalSpacing": true,
                                "labelsEnabled": false
                            },

                            "dataSets": [{
                                "color": "#0192ee",//"#FFA500",
                                //"title": "first data set",
                                "fieldMappings": [{
                                    "fromField": "value",
                                    "toField": "value"
                                }],
                                "dataProvider": data,
                                "categoryField": "date",
                                "dataDateFormat": "YYYY-MM-DD",

                                "categoryAxis": {
                                    "parseDates": true,
                                    "axisAlpha": 0,
                                    "gridAlpha": 0,
                                    "autoGridCount": false,
                                    //"axisColor": "#ff0000",
                                    "gridAlpha": 0,
                                    //"gridColor": "#ff0000",
                                    "gridCount": 0,
                                    "labelsEnabled": false
                                },
                            }],

                            "panels": [{
                                // "showCategoryAxis": false,
                                "title": "Value",
                                "percentHeight": 50,


                                "stockGraphs": [
                                    {
                                        "id": "g1",
                                        "valueField": "value",
                                        "comparable": false,
                                        "compareField": "Open",
                                        //"balloonText": "[[value]]",
                                        //"compareGraphBalloonText": "[[value]]",
                                        "lineThickness": 2,
                                        "fillAlphas": 0.4,

                                    },
                                ],
                            }],

                            "panelsSettings": {
                                //"marginLeft": 0, // inside: false requires that to gain some space
                                //"marginRight": 2
                            },


                            "chartScrollbarSettings": {
                                //"graph": "g1"
                                "enabled": false
                            },

                            "valueAxesSettings": {

                                "labelsEnabled": false
                            },

                            "valueAxes": [{
                                "axisAlpha": -1,
                                "gridAlpha": -5,
                                "labelsEnabled": false,
                            }],

                            "chartCursorSettings": {
                                "enabled": false,
                                "categoryBalloonEnabled": false,
                                "valueBalloonsEnabled": false,
                                "fullWidth": false,

                            },

                            "dataSetSelector": {
                                "divId": "selector"
                            },

                            "export": {
                                "enabled": true
                            }
                        });

                        AmCharts.checkEmptyData = function (chart) {
                            if (0 == chart.dataSets[0].dataProvider.length) {

                                $('#div' + sc).html('');
                                $('#div' + sc).text('No data');
                                //$('#div' + sc).addClass('loadGraphCss');
                            }
                        }

                        AmCharts.checkEmptyData(chart);
                    }
                    catch (e) {

                    }
                }
            
            }
          
            return {
                //initializeClient: initializeClient,
                setCallbacks: setCallbacks,
                FactDropDownChnaged: FactDropDownChnaged,
                graphEq: graphEq
              
            }
        } catch (e) {
            console.log("...eee....", e)
        }
    }

    return stockTickerOperations;
}]);

app.directive('amChart', ['$q', function ($q) {
    console.log("chart draw");
    return {
        restrict: 'E',
        replace: true,
        scope: {
            options: '=',
            chart: '=?',
            height: '@',
            width: '@',
            id: '@'
        },
        template: '<div class="amchart"></div>',
        link: function ($scope, $el, element) {

            $scope.$watch('options', function () {
                var id = getIdForUseInAmCharts();
                $el.attr('id', id);
                var chart;
                $scope.chart = chart;

                // allow $scope.options to be a promise
                $q.when($scope.options).then(function (options) {
                    // we can't render a chart without any data
                    if (options.data) {
                        var renderChart = function (amChartOptions) {
                            var o = amChartOptions ? amChartOptions.$$state ? amChartOptions.$$state.value : amChartOptions || options : amChartOptions || options;

                            // set height and width
                            var height = $scope.height || '100%';
                            var width = $scope.width || '100%';

                            $el.css({
                                'height': height,
                                'width': width
                            });

                            // instantiate new chart object
                            if (o.type === 'xy') {
                                chart = o.theme ? new AmCharts.AmXYChart(AmCharts.themes[o.theme]) : new AmCharts.AmXYChart();
                            } else if (o.type === 'pie') {
                                chart = o.theme ? new AmCharts.AmPieChart(AmCharts.themes[o.theme]) : new AmCharts.AmPieChart();
                            } else if (o.type === 'funnel') {
                                chart = o.theme ? new AmCharts.AmFunnelChart(AmCharts.themes[o.theme]) : new AmCharts.AmFunnelChart();
                            } else if (o.type === 'radar') {
                                chart = o.theme ? new AmCharts.AmRadarChart(AmCharts.themes[o.theme]) : new AmCharts.AmRadarChart();
                            } else if (o.type === 'gauge') {
                                chart = o.theme ? new AmCharts.AmAngularGauge(AmCharts.themes[o.theme]) : new AmCharts.AmAngularGauge();
                            } else {
                                chart = o.theme ? new AmCharts.AmSerialChart(AmCharts.themes[o.theme]) : new AmCharts.AmSerialChart();
                            }

                            /** set some default values that amCharts doesnt provide **/
                            $q.when(o.data)
                              .then(function (data) {

                                  chart.dataProvider = data;
                                  // if a category field is not specified, attempt to use the first field from an object in the array
                                  if (o.type != 'gauge') {
                                      chart.categoryField = o.categoryField || Object.keys(o.data[0])[0];
                                  }
                                  //chart.startDuration = 0.5; // default animation length, because everyone loves a little pizazz

                                  // AutoMargin is on by default, but the default 20px all around seems to create unnecessary white space around the control
                                  chart.autoMargins = true;
                                  chart.marginTop = 5;
                                  chart.marginLeft = 0;
                                  chart.marginBottom = 0;
                                  chart.marginRight = 5;

                                  // modify default creditsPosition
                                  chart.creditsPosition = 'top-right';

                                  function generateGraphProperties(data) {
                                      // Assign Category Axis Properties
                                      if (o.categoryAxis) {
                                          var categoryAxis = chart.categoryAxis;

                                          if (categoryAxis) {
                                              /* if we need to create any default values, we should assign them here */
                                              categoryAxis.parseDates = true;

                                              var keys = Object.keys(o.categoryAxis);
                                              for (var i = 0; i < keys.length; i++) {
                                                  if (!angular.isObject(o.categoryAxis[keys[i]]) || angular.isArray(o.categoryAxis[keys[i]])) {
                                                      categoryAxis[keys[i]] = o.categoryAxis[keys[i]];
                                                  } else {
                                                      console.log('Stripped categoryAxis obj ' + keys[i]);
                                                  }
                                              }
                                              chart.categoryAxis = categoryAxis;
                                          }
                                      }

                                      // Create value axis

                                      /* if we need to create any default values, we should assign them here */

                                      var addValueAxis = function (a) {
                                          var valueAxis = new AmCharts.ValueAxis();

                                          var keys = Object.keys(a);
                                          for (var i = 0; i < keys.length; i++) {
                                              valueAxis[keys[i]] = a[keys[i]];
                                          }
                                          chart.addValueAxis(valueAxis);
                                      };

                                      if (o.valueAxes && o.valueAxes.length > 0) {
                                          for (var i = 0; i < o.valueAxes.length; i++) {
                                              addValueAxis(o.valueAxes[i]);
                                          }
                                      }

                                      //reusable function to create graph
                                      var addGraph = function (g) {
                                          var graph = new AmCharts.AmGraph();
                                          /** set some default values that amCharts doesnt provide **/
                                          // if a category field is not specified, attempt to use the second field from an object in the array as a default value
                                          if (g && o.data && o.data.length > 0) {
                                              graph.valueField = g.valueField || Object.keys(o.data[0])[1];
                                          }
                                          graph.balloonText = '<span style="font-size:14px">[[category]]: <b>[[value]]</b></span>';
                                          if (g) {
                                              var keys = Object.keys(g);
                                              // iterate over all of the properties in the graph object and apply them to the new AmGraph
                                              for (var i = 0; i < keys.length; i++) {
                                                  graph[keys[i]] = g[keys[i]];
                                              }
                                          }
                                          chart.addGraph(graph);
                                      };

                                      if (o.type == 'gauge') {
                                          if (o.axes && o.axes.length > 0) {
                                              for (var i = 0; i < o.axes.length; i++) {
                                                  var axis = new AmCharts.GaugeAxis();
                                                  Object.assign(axis, o.axes[i]);
                                                  chart.addAxis(axis);
                                              }
                                          }
                                          if (o.arrows && o.arrows.length > 0) {
                                              for (var i = 0; i < o.arrows.length; i++) {
                                                  var arrow = new AmCharts.GaugeArrow();
                                                  Object.assign(arrow, o.arrows[i]);
                                                  chart.addArrow(arrow);
                                              }
                                          }
                                      }
                                      else {
                                          // create the graphs
                                          if (o.graphs && o.graphs.length > 0) {
                                              for (var i = 0; i < o.graphs.length; i++) {
                                                  addGraph(o.graphs[i]);
                                              }
                                          } else {
                                              addGraph();
                                          }
                                      }

                                      if (o.type === 'gantt' || o.type === 'serial' || o.type === 'xy') {
                                          var chartCursor = new AmCharts.ChartCursor();
                                          if (o.chartCursor) {
                                              var keys = Object.keys(o.chartCursor);
                                              for (var i = 0; i < keys.length; i++) {
                                                  if (typeof o.chartCursor[keys[i]] !== 'object') {
                                                      chartCursor[keys[i]] = o.chartCursor[keys[i]];
                                                  }
                                              }
                                          }
                                          chart.addChartCursor(chartCursor);
                                      }

                                      if (o.chartScrollbar) {
                                          var scrollbar = new AmCharts.ChartScrollbar();
                                          var keys = Object.keys(o.chartScrollbar);
                                          for (var i = 0; i < keys.length; i++) {
                                              scrollbar[keys[i]] = o.chartScrollbar[keys[i]];
                                          }
                                          chart.chartScrollbar = scrollbar;
                                      }

                                      if (o.balloon) {
                                          chart.balloon = o.balloon;
                                      }
                                  }

                                  function generatePieProperties() {
                                      if (o.balloon) {
                                          chart.balloon = o.balloon;
                                      }
                                      if (o.balloonFunction) {
                                          chart.balloonFunction = o.balloonFunction;
                                      }
                                  }

                                  if (o.legend) {
                                      var legend = new AmCharts.AmLegend();
                                      var keys = Object.keys(o.legend);
                                      for (var i = 0; i < keys.length; i++) {
                                          legend[keys[i]] = o.legend[keys[i]];
                                      }
                                      chart.legend = legend;
                                  }

                                  if (o.type === 'pie') {
                                      generatePieProperties();
                                  } else {
                                      generateGraphProperties();
                                  }

                                  if (o.titles) {
                                      for (var i = 0; i < o.titles.length; i++) {
                                          var title = o.titles[i];
                                          chart.addTitle(title.text, title.size, title.color, title.alpha, title.bold);
                                      };
                                  }

                                  if (o.allLabels) {
                                      chart.allLabels = o.allLabels;
                                  }

                                  if (o.labelFunction) {
                                      chart.labelFunction = o.labelFunction;
                                  }

                                  if (o.export) {
                                      chart.amExport = o.export;
                                      chart.export = o.export;
                                  }

                                  if (o.responsive) {
                                      chart.responsive = o.responsive;
                                  }

                                  if (o.colors) {
                                      chart.colors = o.colors;
                                  }

                                  if (o.defs) {
                                      chart.defs = o.defs;
                                  }

                                  if (o.listeners) {
                                      for (var i = 0; i < o.listeners.length; i++) {
                                          chart.addListener(o.listeners[i].event, o.listeners[i].method);
                                      }
                                  }

                                  var addEventListeners = function (obj, chartObj) {
                                      for (var i = 0; i < obj.length; i++) {
                                          if (obj[i].listeners) {
                                              var listeners = obj[i].listeners;
                                              for (var l = 0; l < listeners.length; l++) {
                                                  chartObj[i].addListener(listeners[l].event, listeners[l].method);
                                              }
                                          }
                                      }
                                  };

                                  var chartKeys = Object.keys(o);
                                  for (var i = 0; i < chartKeys.length; i++) {
                                      if (typeof o[chartKeys[i]] !== 'object' && typeof o[chartKeys[i]] !== 'function') {
                                          chart[chartKeys[i]] = o[chartKeys[i]];
                                      } else if (typeof o[chartKeys[i]] === 'object') {
                                          addEventListeners(o[chartKeys[i]], chart[chartKeys[i]]);
                                      }
                                  }

                                  // WRITE
                                  chart.write(id);
                                  $scope.chart = chart;

                              });
                        }; //renderchart


                        // Render the chart
                        renderChart();


                        // EVENTS =========================================================================

                        //var onAmChartsTriggerChartAnimate = $scope.$on('amCharts.triggerChartAnimate', function (event, id) {
                        //    if (id === $el[0].id || !id) {
                        //        chart.animateAgain();
                        //    }
                        //});

                        var onAmChartsUpdateData = $scope.$on('amCharts.updateData', function (event, data, id) {
                            if (id === $el[0].id || !id) {
                                if ($scope.options.type == 'gauge') {
                                    if (!Array.isArray(data)) data = [data]
                                    for (var i = 0; i < data.length; i++) {
                                        chart.arrows[i] && chart.arrows[i].setValue && chart.arrows[i].setValue(data[i]);
                                    }
                                }
                                else {
                                    chart.dataProvider = data.data;
                                    chart.validateData();
                                }
                            }

                        });

                        var onAmChartsValidateNow = $scope.$on('amCharts.validateNow', function (event, validateData, skipEvents, id) {
                            if (id === $el[0].id || !id) {
                                chart.validateNow(validateData === undefined ? true : validateData,
                                  skipEvents === undefined ? false : skipEvents);
                            }
                        });

                        var onAmChartsRenderChart = $scope.$on('amCharts.renderChart', function (event, amChartOptions, id) {
                            if (id === $el[0].id || !id) {
                                chart.clear();
                                renderChart(amChartOptions);
                            }
                        });

                        $scope.$on('$destroy', function () {
                            chart.clear();
                          
                            onAmChartsUpdateData();
                            onAmChartsValidateNow();
                            onAmChartsRenderChart();
                        });
                    }
                });
                function getIdForUseInAmCharts() {
                    var id = $scope.id;// try to use existing outer id to create new id

                    if (!id) {//generate a UUID
                        var guid = function guid() {
                            function s4() {
                                return Math.floor((1 + Math.random()) * 0x10000)
                                    .toString(16)
                                    .substring(1);
                            }

                            return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                                s4() + '-' + s4() + s4() + s4();
                        };
                        id = guid();
                    }
                    return id;
                }
            })




        }
    };


}]);