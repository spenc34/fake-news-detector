<!-- JavaScript -->
<script>
	import axios from 'axios';
	import GaugeChart from 'gauge-chart';
	import { onMount } from 'svelte';
	const serverBaseUrl = 'http://localhost';
	const serverPort = 3000;

	const colors = {
		white: 'rgb(230, 230, 230)',
		green: '#009933',
		yellow: '#ffe066',
		red: '#cc0000'
	};

	let errorOccurred = false;
	let header = '';
	let title = '';
	let loading = true;
	let probabilityFake = 0;
	let message = '';
	$: percentCount = (100 * probabilityFake).toFixed(2);
	let percentClass = '';
	let gauge;

	onMount(async () => {
		getPrediction();
	});

	async function getPrediction() {
		loading = true;
		if (document.querySelector('#gauge').querySelector('svg')) {
			// Remove the gauge if it's already been drawn
			document.querySelector('#gauge').querySelector('svg').remove();
		}
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let url = tabs[0].url;
			title = tabs[0].title;
			axios.post(`${serverBaseUrl}:${serverPort}/predict`, {url})
				.then(response => {
					errorOccurred = false;
					probabilityFake = response.data.probabilityFake;
					if (probabilityFake === 0) {
						percentClass = 'ok';
						message = 'The news on this site is reliable';
					}
					else if (probabilityFake < 0.5) {
						percentClass = 'ok';
						message = 'The news on this site is probably reliable';
					} else if (probabilityFake < 0.75) {
						percentClass = 'warning';
						message = 'This site may contain false or biased information';
					} else {
						percentClass = 'danger';
						message = 'This site most likely contains false information';
					}
				})
				.catch(error => {
					errorOccurred = true;
					if (!error.response) {
						// network error
						message = 'Error: Could not connect to server';
					} else {
						message = 'Error: Could not get info for this site: ' + error.response.data.message;
					}
				})
				.finally(() => {
					loading = false;
				});
		});
	}

	$: if (!loading) {
		header = 'Fake News Detector';
		let gaugeOptions = {
			hasNeedle: true,
			needleColor: colors.white,
			needleUpdateSpeed: 1500,
			arcColors: [colors.green, colors.yellow, colors.red],
			arcDelimiters: [50, 75],
			arcPadding: 50
		};
		
		GaugeChart.gaugeChart(document.querySelector('#gauge'), 300, gaugeOptions).updateNeedle(percentCount);
	} else {
		header = '';
	}

</script>

<!-- HTML -->
<div id='popup'>
	<div class='header'>{header}</div>
	<div id='gauge'></div>
	{#if !loading}
		<div class='page-title'>{title}</div>
		{#if errorOccurred}
			<div class='message error'>{message}</div>
		{:else}
			<span class='percent {percentClass}'>{percentCount}%</span>
			<div class='message'>{message}</div>
		{/if}
		<button on:click={getPrediction} type="button" class="btn btn-outline-light">Reload</button>
		<div class='disclaimer'>Note: The fake news detector was trained on news sites. Predictions for other sites may be inaccurate.</div>
	{:else}
		<div class="spinner-grow text-light m-5" role="status">
			<span class="sr-only">Loading...</span>
		</div>
	{/if}
</div>

<!-- CSS -->
<style>

div {
	text-align: center;
}
#popup {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 10px 15px;
	min-width: 350px;
	min-height: 450px;
}

#gauge {
	margin-bottom: -40px;
}

.percent {
	font-weight: bolder;
	font-size: 3em;
}

.percent.ok {
	color: #009933
}

.percent.warning {
	color: #ffe066;
}

.percent.danger {
	color: #cc0000;
}

.header {
	color: #99cbe8;
	font-size: 2em;
}

.page-title {
	font-size: 1em;
}

.message {
	font-size: 14px;
}

.btn {
	margin: 15px 0;
}

.disclaimer {
	font-size: 11px;
	font-style: italic;
}

.error {
	color: #cc0000;
}
</style>