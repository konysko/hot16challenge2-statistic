<script>
import { Bubble } from 'vue-chartjs';

export default {
  extends: Bubble,
  props: {
    chartTotalAmountValues: {
      type: Array,
      required: false
    },
    chartVideoValues: {
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
        legend: {
          labels: {
            fontColor: '#888',
            filter: function(item) {
              return !item.text.includes('Filmy na YouTube');
            }
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
                labelString: 'Liczba filmów',
                fontColor: '#888'
              },
              position: 'right'
            },
            {
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
                labelString: 'Zebrana kwota',
                fontColor: '#888'
              }
            }
          ],
          xAxes: [
            {
              ticks: {
                fontColor: '#888',
                stepSize: 1,
                padding: 20,
                callback: (value, index) => {
                  return this.chartLabels[index];
                }
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
        maintainAspectRatio: false,
        tooltips: {
          callbacks: {
            label: function(t, d) {
              if (t.datasetIndex === 1) {
                const dataItem = d.datasets[t.datasetIndex].data.find(
                  (item) => item.x === t.xLabel && item.y === t.yLabel
                );
                return dataItem.video_title;
              } else {
                return d.datasets[t.datasetIndex].label + ': ' + t.yLabel.toFixed(2);
              }
            }
          }
        },
        onClick: (evt, elements) => {
          elements.forEach((item) => {
            if (item._datasetIndex === 1) {
              const dataUrl = this.chartVideoValues[item._index].video_url;
              window.open(dataUrl, '_blank');
            }
          });
        },
        onHover: (event, elements) => {
          elements.forEach((item) => {
            if (item._datasetIndex === 1) {
              event.target.style.cursor = 'pointer';
            } else {
              event.target.style.cursor = 'default';
            }
          });
          if (!elements.length) {
            event.target.style.cursor = 'default';
          }
        }
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
            type: 'bubble',
            label: 'Filmy na YouTube',
            backgroundColor: '#50505050',
            pointStyle: this.chartVideoValues.map((value) => {
              const image = new Image();
              image.src = value.video_thumbnail;
              image.width = value.r * 2;
              image.height = value.r * 2;
              return image;
            }),
            data: this.chartVideoValues
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
