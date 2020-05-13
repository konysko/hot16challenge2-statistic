<script>
import { Line } from 'vue-chartjs';

export default {
  extends: Line,
  props: {
    label: {
      type: String,
      required: true
    },
    chartData: {
      type: Array,
      required: false
    },
    chartLabels: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      gradient: null,
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  mounted() {
    const dataCollection = {
      labels: this.chartLabels,
      datasets: [
        {
          label: this.label,
          backgroundColor: '#d2191980',
          borderColor: '#d21919',
          pointBackgroundColor: 'rgba(0,0,0,0)',
          pointBorderColor: 'rgba(0,0,0,0)',
          pointHoverBorderColor: '#d21919',
          pointHoverBackgroundColor: '#fff',
          pointHoverRadius: 4,
          pointHitRadius: 10,
          pointHoverBorderWidth: 1,
          borderWidth: 1,
          data: this.chartData
        }
      ]
    };
    console.log(dataCollection);

    this.renderChart(dataCollection, this.options);
  }
};
</script>
