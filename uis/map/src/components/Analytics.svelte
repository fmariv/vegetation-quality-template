<script>
	import Map from 'svelte-material-icons/Map.svelte';
	import GeoJSONLayer from '$components/map/GeoJSONLayer.svelte';
	import ForestMonitoring from '$components/analytics/ForestMonitoring.svelte';

	export let analytics;
	export let aoi;
	export let date;
	export let xyz_url;
	export let api_url;
	export let left;

	let selected = false;
	const toggleAOI = () => {
		selected = !selected;
	};
</script>

<div>
	<h1>Asset</h1>
	<button
		class={`w-10 h-10 p-1 hover:bg-gray-100 'text-gray-800'} tooltip tooltip-bottom ${
			selected ? 'text-green-600' : 'text-gray-800'
		}`}
		on:click={toggleAOI}
		data-tip="Area of Interest"
	>
		<Map size="100%" />
	</button>
	<h1>Monitoring of</h1>
	<ForestMonitoring {analytics} {date} {xyz_url} {api_url} {left} />
</div>

{#if selected}
	<GeoJSONLayer
		name={'aoi'}
		options={{
			style: { fillOpacity: 0, weight: 3, color: 'blue', dashArray: '' },
			pane: 'aoi',
			zIndex: 0
		}}
		geojson={aoi}
	/>
{/if}
