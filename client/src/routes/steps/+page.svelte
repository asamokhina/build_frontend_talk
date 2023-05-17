<script>
import {
    onMount
} from 'svelte';

import daygridPlugin from '@fullcalendar/daygrid';
import FullCalendar from '$lib/FullCalendar.svelte';

let stepsData = new Map();
let error = null;
let events = [];
let options = new Map();

async function getOptions() {
    try {

        // const response = '{"2023-02-12T00:00:00":{"Actual":13771,"Goal":10000},"2023-02-13T00:00:00":{"Actual":9483,"Goal":10000},"2023-02-14T00:00:00":{"Actual":9520,"Goal":10000}}'
        // const rawDatatest = JSON.parse(response);

        const rawData = await fetch("/data", {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            },
            redirect: "follow",
        }).then((response) => {
            if (response?.ok) {
            return response.json();
            } else {
            return undefined;
            }
        });

        stepsData = rawData;
        setCalendarEvents(stepsData);
        options = {
            events: events,
            initialView: 'dayGridMonth',
            plugins: [daygridPlugin],
        };

    } catch (e) {
        console.error(e);
        error = 'Error fetching data';
    }
}

function setCalendarEvents(stepsData) {

    for (const [date, {
            Actual,
            Goal
        }] of Object.entries(stepsData)) {
        const event = {
            title: `Steps: ${Actual}`,
            start: date,
            allDay: true,
            backgroundColor: getBGColorBySteps(Actual),
            textColor: getTextColorBySteps(Actual),
            borderColor: 'transparent'
        };

        events.push(event);
    }

}

function getTextColorBySteps(steps) {
    if (steps > 10000) {
        return 'white'; // High steps, green color
    } else if (steps > 5000) {
        return '#3f3f3f'; // Moderate steps, yellow color
    } else {
        return 'white'; // Low steps, red color
    }
}

function getBGColorBySteps(steps) {
    if (steps > 10000) {
        return '#8fb935'; // High steps, green color
    } else if (steps > 5000) {
        return '#e6e22e'; // Moderate steps, yellow color
    } else {
        return '#e64747'; // Low steps, red color
    }
}

onMount(getOptions);
</script>

<main>
  {#if stepsData}
    <div class="calendar">
      <FullCalendar
        {options}
      />
    </div>
  {:else}
    <p>Loading data...</p>
  {/if}

</main>
