<script lang="ts">
	import { onMount } from 'svelte';
	import { Calendar } from '@fullcalendar/core';
	import type { CalendarOptions } from '@fullcalendar/core';

	let classes: string | null = null;

	export { classes as class };

	export let style: string | null = null;

	export let options: CalendarOptions;

	export function getAPI() {
		return calendar;
	}

	let calendarEl: HTMLElement;
	let calendar: Calendar;

	onMount(async () => {
		if (!canBeInitiated) return;

		initCalendar();

		return () => {
			calendar && calendar.destroy();
		};
	});

	$: canBeInitiated =
		options && options.plugins && options.plugins.length && calendarEl && !calendar;

	$: {
		if (calendar && options && options.plugins && options.plugins.length) updateCalendarOptions();

		if (canBeInitiated) {
			initCalendar();
		}
	}

	function initCalendar() {
		calendar = new Calendar(calendarEl, options);
		calendar.render();
	}

	function updateCalendarOptions() {
		calendar.pauseRendering();
		calendar.resetOptions(options);
		calendar.resumeRendering();
	}
</script>

<div bind:this={calendarEl} class={classes} {style} />