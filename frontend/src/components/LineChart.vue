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
      barGradient: null,
      options: {
        legend: {
          labels: {
            fontColor: '#888'
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                fontColor: '#888',
                beginAtZero: true,
                callback: (value) => {
                  return this.formatNumber(value);
                }
              },
              scaleLabel: {
                display: true,
                labelString: 'Liczba filmów'
              },
              position: 'right'
            },
            {
              type: 'linear',
              id: 'total-amount',
              ticks: {
                fontColor: '#888',
                beginAtZero: true,
                callback: (value) => {
                  return this.formatNumber(value);
                }
              },
              scaleLabel: {
                display: true,
                labelString: 'Zebrana kwota'
              }
            }
          ],
          xAxes: [
            {
              ticks: {
                fontColor: '#888'
              },
              scaleLabel: {
                display: true,
                labelString: 'Czas',
                fontColor: '#888'
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
            backgroundColor: this.gradient,
            borderColor: '#707070',
            pointBackgroundColor: 'rgba(0,0,0,0)',
            pointBorderColor: 'rgba(0,0,0,0)',
            pointHoverBorderColor: '#505050',
            pointHoverBackgroundColor: '#fff',
            pointHoverRadius: 4,
            pointHitRadius: 10,
            pointHoverBorderWidth: 1,
            borderWidth: 1,
            data: this.chartTotalAmountValues
          },
          {
            label: 'Liczba filmów na YouTube',
            backgroundColor: this.barGradient,
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
    this.gradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 450);
    this.gradient.addColorStop(0, '#50505070');
    this.gradient.addColorStop(0.5, '#50505030');
    this.gradient.addColorStop(1, '#50505000');
    this.barGradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 450);
    this.barGradient.addColorStop(0, '#de4000b0');
    this.barGradient.addColorStop(0.5, '#de400050');
    this.barGradient.addColorStop(1, '#de400010');

    this.renderChart(this.dataCollection, this.options);
  },
  methods: {
    formatNumber(num) {
      let numString = Math.round(num).toString();
      let numberFormatMapping = [
        [6, 'm'],
        [3, 'k']
      ];
      for (let [numberOfDigits, replacement] of numberFormatMapping) {
        if (numString.length > numberOfDigits) {
          let decimal = '';
          if (numString[numString.length - numberOfDigits] !== '0') {
            decimal = '.' + numString[numString.length - numberOfDigits];
          }
          numString = numString.substr(0, numString.length - numberOfDigits) + decimal + replacement;
          break;
        }
      }
      return numString;
    }
  }
};
</script>
