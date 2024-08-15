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
        src: url('https://github.com/johannesaschoff/cs_demonstration/blob/main/source_code.py') format('opentype');
        font-weight: normal;
        font-style: normal;
    }

    body {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        height: 100vh;
        margin: 0;
        padding: 0 50px; /* Added padding for left margin */
        font-family: 'UnitSlabOT-Bold', sans-serif;
    }

    #container {
        width: 80%; /* Adjusted width for left margin */
        height: 600px;
        margin-left: 100px; /* Add margin to the left */
    }
    </style>
</head>
<body>
    <div id="container"></div>
    <script>
        // Define the series data with manual colors
        var seriesData = [
            { name: 'Financial Services', data: [2327, 2366, 2265, 1875, 1633], stack: 'EU', id: 'FinancialServices', color: '#21b2d3' },
            { name: 'Support Services (Industrial Goods and Services)', data: [1682, 1837, 1922, 1453, 1178], stack: 'EU', id: 'SupportServicesIndustrialGoodsandServices', color: '#59beda' },
            { name: 'Retail', data: [2592, 2675, 2361, 1650, 1135], stack: 'EU', id: 'Retail', color: '#d2e8f5' },
            { name: 'Construction and Materials', data: [1425, 1500, 1641, 1282, 1110], stack: 'EU', id: 'ConstructionandMaterials', color: '#80cee5' },
            { name: 'Food and Beverage', data: [1953, 2045, 2073, 1443, 1025], stack: 'EU', id: 'FoodandBeverage', color: '#828181' },
            { name: 'Financial Services', data: [602, 516, 459, 511, 536], stack: 'GB', linkedTo: 'FinancialServices', color: 'rgb(33,178,211,0.2)' },
            { name: 'Oil and Gas', data: [378, 414, 366, 385, 375], stack: 'GB', id: 'OilandGas', color: 'rgb(6,164,204,0.2)' },
            { name: 'Retail', data: [305, 308, 327, 345, 298], stack: 'GB', linkedTo: 'Retail', color: 'rgb(210,232,245,0.2)' },
            { name: 'Support Services (Industrial Goods and Services)', data: [383, 282, 0, 281, 290], stack: 'GB', linkedTo: 'SupportServicesIndustrialGoodsandServices', color: 'rgb(89,190,218,0.2)' },
            { name: 'Mining', data: [0, 0, 253, 253, 217], stack: 'GB', id: 'Mining', color: 'rgb(197,192,184,0.2)' },
            { name: 'Food and Beverage', data: [233, 229, 250, 0, 0], stack: 'GB', linkedTo: 'FoodandBeverage', color: 'rgb(130,129,129,0.2)' },
            { name: 'Relative Change in Incidents United Kingdom', type: 'spline', yAxis: 1, data: [0.0, 3.43822843822843, -6.760563380281692, 5.679758308157101, 8.690680388793592], tooltip: { valueSuffix: '%' }, color: '#E32553' },
            { name: 'Relative Change in Incidents Europe', type: 'spline', yAxis: 1, data: [0.0, 26.67324453214932, 33.22082305595222, 1.568894952251032, -4.259810035498413], tooltip: { valueSuffix: '%' }, color: '#7D9AAA' }
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
                            'logo/RR_DBlue_Hor_rgb.png', // Path to your logo
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
                align: 'left',  // Align title to the left
                x: 200, // Move the title to the right
                style: {
                    fontFamily: 'UnitSlabOT-Bold'
                }
            },
            subtitle: {
                text: 'Global ESG risk incidents for companies headquartered in the UK',
                align: 'left',  // Align subtitle to the left
                x: 200, // Move the subtitle to the right
                style: {
                    fontFamily: 'inherit'
                }
            },
            xAxis: [{
                categories: [2024, 2023, 2022, 2021, 2020],
                crosshair: true,
                labels: {
                    style: {
                        fontFamily: 'inherit'
                    },
                    formatter: function() {
                        return this.value + '<br><span style="color: #000000;">UK   </span>   <span style="color: #000000;">   EU</span>';
                    }
                }
            }],
            yAxis: [{ 
                min: 0,
                title: {
                    text: 'Percentage (%)',
                    style: {
                        fontFamily: 'inherit'
                    }
                }
            }, { 
                title: {
                    text: 'Relative Change in Total Incidents',
                    style: {
                        fontFamily: 'inherit'
                    }
                },
                labels: {
                    format: '{value}%',
                    style: {
                        fontFamily: 'inherit'
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true,
                useHTML: true,
                backgroundColor: '#000000',  // Black background for the tooltip
                style: {
                    color: '#FFFFFF',  // White text for readability
                    fontFamily: 'inherit'
                },
                headerFormat: '<span style="font-size: 10px; color: #FFFFFF;">{point.key}</span><br/>',
                pointFormatter: function() {
                    var value = Math.round(this.y); // Round the value to the nearest integer
                    return '<span style="color:' + '#FFFFFF' + '; font-family: inherit;">' + this.series.name + '</span>: <b>' + value + (this.series.tooltipOptions.valueSuffix || '') + '</b><br/>';
                }
            },

            plotOptions: {
                column: {
                    stacking: 'percent',
                    pointPadding: 0.1,  // Reduce the space between individual bars within the same group
                    groupPadding: 0.1   // Reduce the space between different groups of bars
                }
            },
            series: seriesData,
            credits: {
                enabled: false // Disable the Highcharts text in the bottom right
            },
            exporting: {
                enabled: false // Disable the chart context menu
            }
        });
    </script>
</body>
</html>



    """
elif slide == "Slide 2":
    highcharts_html = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Chart with Stacked IDs</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <style>
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    #container {
        width: 80%;
        height: 600px;
    }
    </style>
</head>
<body>
    <div id="container"></div>
    <script>
        // Define the series data with manual colors
        var seriesData = [
            { name: 'Financial Services', data: [536   , 511, 458, 516, 577], stack: 'GB', id: 'FinancialServices', color: '#00B9E4' },
            { name: 'Financial Services (EU)', data: [1604  ,  1856  ,  2250   , 2336 ,   2219], stack: 'EU', linkedTo: 'FinancialServices', color: '#00B9E4' },
            { name: 'Construction and Materials', data: [1110,   1283,    1644 ,   1499,    1390], stack: 'EU', id: 'C&M', color: '#A3DBE8' },
            { name: 'Food and Beverage', data: [0,0,250, 229, 227], stack: 'GB', id: 'F&B', color: '#8FCB9B' },
            { name: 'Food and Beverage (EU)', data: [1027   , 1443  ,  2073   , 2045   , 1886], stack: 'EU', linkedTo: 'F&B', color: '#8FCB9B' },
            { name: 'Retail', data: [298    ,345 ,327 ,308 ,300], stack: 'GB', id: 'Retail', color: '#5B9279' },
            { name: 'Retail (EU)', data: [1129, 1638, 2358, 2672, 2506], stack: 'EU', linkedTo: 'Retail', color: '#5B9279' },
            { name: 'Industrial Goods and Services', data: [290 ,281 ,0,283 ,369], stack: 'GB', id: 'Support Services', color: '#E0E1DD' },
            { name: 'Industrial Goods and Services (EU)', data: [1176  ,  1446    ,1907   , 1789    ,1626], stack: 'EU', linkedTo: 'Support Services', color: '#E0E1DD' },
            { name: 'Mining', data: [217,    253, 253,0,0], stack: 'GB', id: 'Mining', color: '#A9AAA9' },
            { name: 'Oil and Gas', data: [375   ,385 ,366 ,414 ,369], stack: 'GB', id: 'O&G', color: '#565A5C' },
            { name: 'Relative Change in Incidents Europe', type: 'spline', yAxis: 1, data: [15270, 18394, 23168, 23567, 22431], tooltip: { valueSuffix: '%' }, id: 'Temperature', color: '#7D9AAA' },
            { name: 'Relative Change in Incidents United Kingdom', type: 'spline', yAxis: 1, data: [3384, 3500, 3316, 3550, 4001], tooltip: { valueSuffix: '%' }, id: 'EUTemperature', color: '#E32553' }
        ];

        // Function to normalize data to show relative change from the first value
        function normalizeData(data) {
            return data.map((value, index) => {
                if (index === 0) return 0;
                return ((value - data[0]) / data[0]) * 100;
            });
        }

        // Normalize Temperature and EU Temperature data
        seriesData.forEach(series => {
            if (series.id === 'Temperature' || series.id === 'EUTemperature') {
                series.data = normalizeData(series.data);
                series.tooltip.valueSuffix = '%'; // Update the tooltip suffix to reflect percentage change
            }
        });

        // Render the chart
        Highcharts.chart('container', {
            chart: {
                type: 'column',
                zooming: {
                    type: 'xy'
                }
            },
            title: {
                text: 'Five riskiest sectors in the UK compared to Europe',
                align: 'center'
            },
            subtitle: {
                text: 'Global ESG risk incidents for companies headquartered in the UK',
                align: 'center'
            },
            xAxis: [{
                categories: ['2020', '2021', '2022', '2023', '2024'],
                crosshair: true,
                labels: {
                    formatter: function() {
                        return this.value + '<br><span style="color: #000000;">UK   </span>   <span style="color: #000000;">   EU</span>';
                    }
                }
            }],
            yAxis: [{ 
                min: 0,
                title: {
                    text: 'Percentage (%)'
                }
            }, { 
                title: {
                    text: 'Relative Change in Total Incidents'
                },
                labels: {
                    format: '{value}%'
                },
                opposite: true
            }],
            tooltip: {
                shared: true,
                useHTML: true,
                pointFormatter: function() {
                    var value = Math.round(this.y); // Round the value to the nearest integer
                    return '<span style="color:' + this.color + '">' + this.series.name + '</span>: <b>' + value + (this.series.tooltipOptions.valueSuffix || '') + '</b><br/>';
                }
            },

            plotOptions: {
                column: {
                    stacking: 'percent'
                }
            },
            series: seriesData
        });
    </script>
</body>
</html>

    """
elif slide == "Slide 3":
    highcharts_html = """<Insert your third HTML graph here>"""

# Embed the selected Highcharts graph in Streamlit
components.html(highcharts_html, height=1000)
