<script>
import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  props: {
    chartTotalAmountValues: {
      type: Array,
      required: false
    },
    chartVideoCountValues: {
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
              },
              scaleLabel: {
                display: true,
                labelString: 'Liczba wideo'
              },
              position: 'right'
            },
            {
              type: 'linear',
              id: 'total-amount',
              ticks: {
                beginAtZero: true
              },
              scaleLabel: {
                display: true,
                labelString: 'Kwota'
              }
            }
          ]
        },
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  computed: {
    dataCollection() {
      return {
        labels: this.chartLabels,
        datasets: [
          {
            type: 'line',
            yAxisID: 'total-amount',
            label: 'Całkowita zebrana kwota',
            backgroundColor: '#27272750',
            borderColor: '#272727',
            pointBackgroundColor: 'rgba(0,0,0,0)',
            pointBorderColor: 'rgba(0,0,0,0)',
            pointHoverBorderColor: '#272727',
            pointHoverBackgroundColor: '#fff',
            pointHoverRadius: 4,
            pointHitRadius: 10,
            pointHoverBorderWidth: 1,
            borderWidth: 1,
            data: this.chartTotalAmountValues
          },
          {
            label: 'Liczba wideo na YouTube',
            backgroundColor: '#27272750',
            data: this.chartVideoCountValues
          }
        ]
      };
    }
  },
  watch: {
    dataCollection() {
      this.renderChart(this.dataCollection, this.options);
    }
  },
  mounted() {
    this.renderChart(this.dataCollection, this.options);
  }
};
</script>
