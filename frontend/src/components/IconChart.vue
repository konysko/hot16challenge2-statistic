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
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              scaleLabel: {
                display: true,
                labelString: 'Wideo'
              },
              position: 'right'
            },
            {
              id: 'total-amount',
              ticks: {
                beginAtZero: true
              },
              scaleLabel: {
                display: true,
                labelString: 'Kwota'
              }
            }
          ],
          xAxes: [
            {
              ticks: {
                min: -1,
                max: 24,
                stepSize: 1,
                padding: 20
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
            type: 'bubble',
            label: 'Wideo na YouTube',
            backgroundColor: '#27272750',
            pointStyle: this.chartVideoValues.map((value) => {
              const image = new Image();
              image.src = value.video_thumbnail;
              image.width = 30;
              image.height = 30;
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
    this.renderChart(this.dataCollection, this.options);
  }
};
</script>
