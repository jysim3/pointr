<template>
    <div>
        <div class="img-container">
        <img src="../assets/logo.png" alt="pointr logo">
        </div>
        <div class="chart-wrapper">
            <h1 class="title"> Population graph </h1>
            <canvas id="myChart" width="400" height="400"></canvas>
        </div>
    </div>
</template>

<script>
import Chart from 'chart.js';
export default {
    name: "Statistics",
    mounted() {
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['9:00am','9:30am','10:00am','10:30am','11:00am','11:30am','12:00am',],
                datasets: [{
                    label: 'Number of attendees at a given time',
                    data: [12, 19, 3, 5, 2, 3],
                    fill: false,
                    backgroundColor: 
                        'rgba(255, 99, 132, 0.2)',
                    borderColor: 
                        'rgba(255, 99, 132, 1)',
                    
                    borderWidth: 1
                }]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
            /* eslint-disable no-console */
            console.log(myChart);
            /* eslint-enable no-console */

    }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css?family=Open+Sans:400,600,700|Raleway&display=swap');

.title { 
    font-family: 'Raleway', Helvetica, Arial, sans-serif;
    text-transform: capitalize;
    font-weight: 700;
    font-size: 3rem;
    text-align: left;
    color: black;
    margin-top: 0;
}
.chart-wrapper {

    display: block;
    margin: auto;
    margin-top: 70px;

    max-width: 25rem;
    position: relative;
    padding: 30px 30px;
    box-shadow: 0 0 2rem 0 rgba(59,59,95,.3);
    overflow: hidden;
    max-height: 1000px;
    border-radius: 10px;
    background-color: white;
}
</style>