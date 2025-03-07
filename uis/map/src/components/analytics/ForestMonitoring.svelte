<script>
	import Sprout from 'svelte-material-icons/Sprout.svelte';
	import TrendingUp from 'svelte-material-icons/TrendingUp.svelte';
	import Pie from '$components/viz/Pie.svelte';
	import ImageLayer from '$components/map/ImageLayer.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';

	export let title;
	export let analytics;
	export let date;
	export let xyz_url;
	export let api_url;
	export let left;

	$: title = $currentAnalytic;
	$: image = 'vegetation_masked_';
	$: bands = [1];
	$: stretch = [0, 1];
	$: palette = 'RdYlGn';

	let selectedButton = 'growth';
	let selected = true;

	let options = {};
	$: if (analytics && date && title === 'Vegetation Growth') {
		options = {
			series: [analytics['Vegetation Ha'][date], analytics['Not Vegetation Ha'][date]],
			labels: ['Vegetation Ha', 'Not Vegetation Ha'],
			tooltip: {
				y: {
					formatter: function (value) {
						return parseInt(value).toLocaleString('en-US') + ' Has';
					}
				}
			},
			dataLabels: {
				formatter: function (val, opts) {
					return parseInt(0.01 * val * analytics.Total[date]).toLocaleString('en-US');
				}
			},
			colors: ['#25dd47', '#ff0000'],
			plotOptions: {
				pie: {
					donut: {
						labels: {
							show: true,
							value: {
								formatter: function (v) {
									return Number.parseInt(v).toLocaleString('en-US') + 'Has';
								}
							},
							total: {
								show: true,
								label: 'Total',
								color: '#373d3f',
								formatter: function (w) {
									const total = w.globals.seriesTotals.reduce((a, b) => {
										return a + b;
									}, 0);
									return parseInt(total).toLocaleString('en-US') + 'Has';
								}
							}
						}
					}
				}
			},
			legend: {
				position: 'bottom'
			}
		};
	} else if (analytics && date && title === 'Vegetation Health') {
		options = {
			series: [
				analytics['Bare Ground'][date],
				analytics['Healthy Vegetation'][date],
				analytics['Sparse or Unhealthy Vegetation'][date],
				analytics['Very Healthy Vegetation'][date]
			],
			labels: [
				'Bare ground',
				'Healthy Vegetation',
				'Sparse or Unhealthy Vegetation',
				'Very Healthy Vegetation'
			],
			colors: ['#ff0000', '#90ee90', '#ffff00', '#006400'],
			plotOptions: {
				pie: {
					donut: {
						labels: {
							show: true,
							value: {
								formatter: function (v) {
									return Number.parseInt(v).toLocaleString('en-US') + ' Has';
								}
							},
							total: {
								show: true,
								label: 'Total',
								color: '#373d3f',
								formatter: function (w) {
									const total = w.globals.seriesTotals.reduce((a, b) => {
										return a + b;
									}, 0);
									return parseInt(total).toLocaleString('en-US') + ' Has';
								}
							}
						}
					}
				}
			},
			legend: {
				position: 'bottom'
			}
		};
	}

	const fetchQuality = async () => {
		if (selected && $currentAnalytic === 'Vegetation Health') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/AOI_Vegetation_Quality`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Vegetation Health');
		image = 'quality_masked_rgb_';
		bands = [1, 2, 3];
		stretch = [0, 255];
		palette = 'RdYlGn';
		selectedButton = 'quality';
	};

	const fetchGrowth = async () => {
		if (selected && $currentAnalytic === 'Vegetation Growth') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/AOI_Vegetation_Growth`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Vegetation Growth');
		image = 'vegetation_masked_';
		bands = [1];
		stretch = [0, 1];
		palette = 'RdYlGn';
		selectedButton = 'growth';
	};
</script>

<button
	data-tip="Vegetation Growth"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'growth' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fetchGrowth}
>
	<TrendingUp size="100%" />
</button>

<button
	data-tip="Vegetation Health"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'quality' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fetchQuality}
>
	<Sprout size="100%" />
</button>

{#if selected}
	<h3>{title}</h3>
	<Pie {options} height={300} />
{/if}

{#if selected}
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + left + '.tif'}
		options={{
			maxZoom: 20,
			pane: 'left'
		}}
		{bands}
		{stretch}
		{palette}
	/>
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + date + '.tif'}
		options={{
			maxZoom: 20,
			pane: 'right'
		}}
		{bands}
		{stretch}
		{palette}
	/>
{/if}
