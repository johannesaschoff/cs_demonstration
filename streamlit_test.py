import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration to full width
st.set_page_config(layout="wide")

# Create a sidebar menu
st.sidebar.title("Navigation")
slide = st.sidebar.radio("Go to Slide", ["Slide 1", "Slide 2", "Slide 3"])

# Define the HTML for each slide
if slide == "Slide 1":
    highcharts_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figure 1</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <style>
    @font-face {
        font-family: 'UnitSlabOT-Bold';
        src: url('./fonts/UnitSlabOT-Bold.woff2') format('woff2'),
             url('./fonts/UnitSlabOT-Bold.woff') format('woff'),
             url('./fonts/UnitSlabOT-Bold.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
    }

    body {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        height: 100vh;
        margin: 0;
        padding: 0 50px;
        font-family: 'UnitSlabOT-Bold', sans-serif;
    }

    #container {
        width: 80%;
        height: 600px;
        margin-left: 100px;
    }

    .highcharts-title, .highcharts-subtitle {
        font-family: 'UnitSlabOT-Bold', sans-serif !important;
    }
    </style>
</head>
<body>
    <div id="container"></div>
    <script>
        // Define the series data with manual colors
        var seriesData = [
            { name: 'Retail', data: [1365, 1917, 2621, 2906, 2833], stack: 'EU', id: 'Retail', color: 'rgb(210,232,245,0.2)' },
            { name: 'Financial Services', data: [2059, 2281, 2615, 2771, 2830], stack: 'EU', id: 'FinancialServices', color: 'rgb(33,178,211,0.2)' },
            { name: 'Retail', data: [2075, 2253, 2252, 2117, 2652], stack: 'US', linkedTo: 'Retail', color: '#d2e8f5' },
            { name: 'Financial Services', data: [1877, 1821, 1564, 1937, 2465], stack: 'US', linkedTo: 'FinancialServices', color: '#21b2d3' },
            { name: 'Food and Beverage', data: [1122, 1610, 2256, 2202, 2136], stack: 'EU', id: 'FoodandBeverage', color: 'rgb(130,129,129,0.2)' },
            { name: 'Software and Computer Services', data: [1302, 1241, 1256, 1516, 2040], stack: 'US', id: 'SoftwareandComputerServices', color: 'rgba(0, 0, 0, 0.5)' },
            { name: 'Support Services (Industrial Goods and Services)', data: [1427, 1709, 2116, 2086, 2032], stack: 'EU', id: 'SupportServicesIndustrialGoodsandServices', color: 'rgb(89,190,218,0.2)' },
            { name: 'Utilities', data: [0, 0, 0, 0, 1576], stack: 'EU', id: 'Utilities', color: '#000000' },
            { name: 'Support Services (Industrial Goods and Services)', data: [1103, 1083, 894, 1022, 1404], stack: 'US', linkedTo: 'SupportServicesIndustrialGoodsandServices', color: '#59beda' },
            { name: 'Health Care Equipment and Services', data: [0, 0, 0, 0, 1235], stack: 'US', id: 'HealthCareEquipmentandServices', color: 'rgba(0, 0, 0, 0.5)' },
            { name: 'Construction and Materials', data: [1190, 1387, 1750, 1592, 0], stack: 'EU', id: 'ConstructionandMaterials', color: 'rgb(128,206,229,0.2)' },
            { name: 'Food and Beverage', data: [1162, 1343, 1255, 1114, 0], stack: 'US', linkedTo: 'FoodandBeverage', color: '#828181' },
            { name: 'Relative Change in Incidents United Kingdom', type: 'spline', yAxis: 1, data: [0.0, 1.4961585119288356, -6.636311895276037, 5.370641306998292, 26.33497251952559], tooltip: { valueSuffix: '%' }, color: '#E32553' },
            { name: 'Relative Change in Incidents Europe', type: 'spline', yAxis: 1, data: [0.0, 18.442095845216123, 21.547613427128077, 2.509225092250933, 0.6934182107536602], tooltip: { valueSuffix: '%' }, color: '#7D9AAA' }
        ];

        // Render the chart
        Highcharts.chart('container', {
            chart: {
                type: 'column',
                zooming: {
                    type: 'xy'
                },
                events: {
                    load: function() {
                        var chart = this;
                        // Add the logo image
                        chart.renderer.image(
                            'RR_DBlue_Hor_rgb.png', // Path to your logo
                            chart.plotLeft + 0, // Adjust horizontal position to align with title margin
                            0, // Vertical position
                            130, // Width of the logo (adjust as needed)
                            130/2.11 // Height of the logo (adjust as needed, maintain aspect ratio)
                        ).add();
                    }
                }
            },
            title: {
                text: 'Five riskiest sectors in the UK compared to Europe',
                align: 'left',
                x: 200,
                style: {
                    fontFamily: 'UnitSlabOT-Bold',
                    color: '#333',
                    fontWeight: 'normal'
                }
            },
            subtitle: {
                text: 'Global ESG risk incidents for companies headquartered in the UK',
                align: 'left',
                x: 200,
                style: {
                    fontFamily: 'UnitSlabOT-Bold',
                    color: '#666',
                    fontWeight: 'normal'
                }
            },
            xAxis: [{
                categories: [2020, 2021, 2022, 2023, 2024],
                crosshair: true,
                labels: {
                    style: {
                        fontFamily: 'UnitSlabOT-Bold'
                    },
                    formatter: function() {
                        return this.value + '<br><span style="color: #000000;">US   </span>   <span style="color: #000000;">   EU</span>';
                    }
                }
            }],
            yAxis: [{ 
                min: 0,
                title: {
                    text: 'Percentage (%)',
                    style: {
                        fontFamily: 'UnitSlabOT-Bold'
                    }
                }
            }, { 
                title: {
                    text: 'Relative Change in Total Incidents',
                    style: {
                        fontFamily: 'UnitSlabOT-Bold'
                    }
                },
                labels: {
                    format: '{value}%',
                    style: {
                        fontFamily: 'UnitSlabOT-Bold'
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true,
                useHTML: true,
                backgroundColor: '#000000',
                style: {
                    color: '#FFFFFF',
                    fontFamily: 'UnitSlabOT-Bold'
                },
                headerFormat: '<span style="font-size: 10px; color: #FFFFFF;">{point.key}</span><br/>',
                pointFormatter: function() {
                    var value = Math.round(this.y);
                    return '<span style="color:' + '#FFFFFF' + '; font-family: inherit;">' + this.series.name + '</span>: <b>' + value + (this.series.tooltipOptions.valueSuffix || '') + '</b><br/>';
                }
            },

            plotOptions: {
                column: {
                    stacking: 'percent',
                    pointPadding: 0.1,
                    groupPadding: 0.1
                }
            },
            series: seriesData,
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
            }
        });
    </script>
</body>
</html>

    """
elif slide == "Slide 3":
    highcharts_html = """<Insert your third HTML graph here>"""

# Embed the selected Highcharts graph in Streamlit
components.html(highcharts_html, height=1000)
