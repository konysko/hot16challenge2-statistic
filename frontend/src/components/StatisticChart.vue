<script>
  import {Line} from "vue-chartjs";

  export default {
    extends: Line,
    props: {
      chartData: {
        type: Object,
        default: null
      },

    },
    data: () => ({
      options: {
        tooltips: {
          enabled: false,
						mode: 'index',
						position: 'nearest',
        },
        responsive: true,
        scales: {
          x: {
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Day'
            },
            type: 'time',
          },
          y: {
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Value'
            }
          }

        }
      }
    }),
    mounted() {

      this.renderChart(this.chartData);
    }
  }
</script>

<style scoped>

</style>
