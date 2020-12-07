<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="page" >
            <div class="page-main" style="margin-top: 20px;">
                <!-- app-content-->
                <div class="app-content">
                    <div class="side-app">
                        <div class="main-content fixed-header visible-title">
                            <!-- Page content -->
                            <div class="container">
                                <div class="row finance-content">
                                    <div class="col-xl-3 col-md-6">
                                        <div class="card shadow text-center">
                                            <div class="card-body">
                                                <h3 class="mb-3">Gross profit Margin</h3>
                                                <div class="chart-circle" data-value="0.75" data-thickness="10" data-color="#ad59ff">
                                                    <canvas width="240" height="240" style="height: 120px; width: 120px;"></canvas><canvas width="128" height="128"></canvas>
                                                    <div class="chart-circle-value"><div class="text-xxl">75%</div></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6">
                                        <div class="card shadow text-center">
                                            <div class="card-body">
                                                <h3 class="mb-3">Opex Ratio</h3>
                                                <div class="chart-circle" data-value="0.55" data-thickness="10" data-color="#00d9bf">
                                                    <canvas width="240" height="240" style="height: 120px; width: 120px;"></canvas><canvas width="128" height="128"></canvas>
                                                    <div class="chart-circle-value"><div class="text-xxl">55%</div></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6">
                                        <div class="card shadow text-center">
                                            <div class="card-body">
                                                <h3 class="mb-3">Operating Profit Margin</h3>
                                                <div class="chart-circle" data-value="0.30" data-thickness="10" data-color="#fc0">
                                                    <canvas width="240" height="240" style="height: 120px; width: 120px;"></canvas><canvas width="128" height="128"></canvas>
                                                    <div class="chart-circle-value"><div class="text-xxl">30%</div></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-xl-3 col-md-6">
                                        <div class="card shadow text-center">
                                            <div class="card-body">
                                                <h3 class="mb-3">Net Profit Margin</h3>
                                                <div class="chart-circle" data-value="0.45" data-thickness="10" data-color="#00b3ff">
                                                    <canvas width="240" height="240" style="height: 120px; width: 120px;"></canvas><canvas width="128" height="128"></canvas>
                                                    <div class="chart-circle-value"><div class="text-xxl">45%</div></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-xl-9">
                                        <div class="card shadow">
                                            <div class="card-header bg-transparent">
                                                <div class="row align-items-center">
                                                    <div class="col">
                                                        <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                        <h2 class="mb-0">Monthly Net Profit</h2>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="card-body">
                                                <div class="chartjs-size-monitor" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                    <div class="chartjs-size-monitor-expand" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                        <div style="position: absolute; width: 1000000px; height: 1000000px; left: 0; top: 0;"></div>
                                                    </div>
                                                    <div class="chartjs-size-monitor-shrink" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                        <div style="position: absolute; width: 200%; height: 200%; left: 0; top: 0;"></div>
                                                    </div>
                                                </div>
                                                <!-- Chart -->
                                                <canvas id="finance-chart" class="chart-dropshadow h-315 chartjs-render-monitor" width="1264" height="632" style="display: block; height: 316px; width: 632px;"></canvas>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-xl-3">
                                        <div class="">
                                            <div class="">
                                                <div class="row">
                                                    <div class="col-xl-12">
                                                        <div class="card shadow bg-gradient-primary">
                                                            <div class="card-body">
                                                                <div class="widget text-center">
                                                                    <small class="text-white h3">Quick Ratio</small>
                                                                    <h2 class="text-xxl text-white mb-0">0.74</h2>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="card shadow bg-gradient-info">
                                                            <div class="card-body">
                                                                <div class="widget text-center">
                                                                    <small class="text-white h3">Current Ratio</small>
                                                                    <h2 class="text-xxl text-white mb-0">1.68</h2>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="card shadow bg-gradient-success">
                                                            <div class="card-body">
                                                                <div class="widget text-center">
                                                                    <small class="text-white h3">Cash Balance</small>
                                                                    <h2 class="text-xxl text-white mb-0"><i class="fas fa-dollar-sign"></i> 1,35,265</h2>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-xl-6">
                                        <div class="row">
                                            <div class="col-xl-6">
                                                <div class="card shadow">
                                                    <div class="card-header bg-transparent">
                                                        <div class="row align-items-center">
                                                            <div class="col">
                                                                <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                                <h2 class="mb-0">Return On Assets</h2>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="card-body finance-chart">
                                                        <div class="chartjs-size-monitor" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                            <div class="chartjs-size-monitor-expand" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 1000000px; height: 1000000px; left: 0; top: 0;"></div>
                                                            </div>
                                                            <div class="chartjs-size-monitor-shrink" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 200%; height: 200%; left: 0; top: 0;"></div>
                                                            </div>
                                                        </div>
                                                       
                                                        <!-- Chart -->
                                                        <canvas id="finance-chart1" class="chart-dropshadow mt-5 h-200 chartjs-render-monitor" width="1264" height="492" style="display: block; height: 246px; width: 632px;"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-xl-6">
                                                <div class="card shadow">
                                                    <div class="card-header bg-transparent">
                                                        <div class="row align-items-center">
                                                            <div class="col">
                                                                <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                                <h2 class="mb-0">Working Capital Ratio</h2>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="card-body finance-chart">
                                                        <div class="chartjs-size-monitor" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                            <div class="chartjs-size-monitor-expand" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 1000000px; height: 1000000px; left: 0; top: 0;"></div>
                                                            </div>
                                                            <div class="chartjs-size-monitor-shrink" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 200%; height: 200%; left: 0; top: 0;"></div>
                                                            </div>
                                                        </div>
                                                        <!-- Chart -->
                                                        <canvas id="finance-chart2" class="chart-dropshadow mt-5 h-200 chartjs-render-monitor" width="1264" height="492" style="display: block; height: 246px; width: 632px;"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-xl-6">
                                                <div class="card shadow">
                                                    <div class="card-header bg-transparent">
                                                        <div class="row align-items-center">
                                                            <div class="col">
                                                                <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                                <h2 class="mb-0">Return On Equity</h2>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="card-body finance-chart">
                                                        <div class="chartjs-size-monitor" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                            <div class="chartjs-size-monitor-expand" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 1000000px; height: 1000000px; left: 0; top: 0;"></div>
                                                            </div>
                                                            <div class="chartjs-size-monitor-shrink" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 200%; height: 200%; left: 0; top: 0;"></div>
                                                            </div>
                                                        </div>
                                                        <!-- Chart -->
                                                        <canvas id="finance-chart3" class="chart-dropshadow mt-5 h-200 chartjs-render-monitor" width="1264" height="492" style="display: block; height: 246px; width: 632px;"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-xl-6">
                                                <div class="card shadow">
                                                    <div class="card-header bg-transparent">
                                                        <div class="row align-items-center">
                                                            <div class="col">
                                                                <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                                <h2 class="mb-0">Debit Equity Ratio</h2>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="card-body finance-chart">
                                                        <div class="chartjs-size-monitor" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                            <div class="chartjs-size-monitor-expand" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 1000000px; height: 1000000px; left: 0; top: 0;"></div>
                                                            </div>
                                                            <div class="chartjs-size-monitor-shrink" style="position: absolute; left: 0; top: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; visibility: hidden; z-index: -1;">
                                                                <div style="position: absolute; width: 200%; height: 200%; left: 0; top: 0;"></div>
                                                            </div>
                                                        </div>
                                                        <!-- Chart -->
                                                        <canvas id="finance-chart4" class="chart-dropshadow mt-5 h-200 chartjs-render-monitor" width="1264" height="492" style="display: block; height: 246px; width: 632px;"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-xl-6">
                                        <div class="card shadow">
                                            <div class="card-header bg-transparent">
                                                <div class="row align-items-center">
                                                    <div class="col">
                                                        <h6 class="text-uppercase text-light ls-1 mb-1">Overview</h6>
                                                        <h2 class="mb-0">Balance sheet</h2>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="">
                                                <div class="card-body">
                                                    <div class="grid-margin">
                                                        <div class="">
                                                            <BalanceSheetComponent></BalanceSheetComponent>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- app-content-->
            </div>
        </div>
    </div>
</template>

<script>
import NavbarComponent from '../NavbarComponent'
import BalanceSheetComponent from './BalanceSheetComponent'
export default {
    components: {
        NavbarComponent,
        BalanceSheetComponent
    }
}
</script>

<style scoped>

</style>