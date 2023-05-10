<script>
import {
    onMount
} from 'svelte';

let stepsData = null;
let error = null;

let showTable = true;

function toggleTable() {
    showTable = !showTable;
}

async function fetchData() {
    try {

        const response = ' {"2023-02-12T00:00:00":{"Actual":13771,"Goal":10000},"2023-02-13T00:00:00":{"Actual":9483,"Goal":10000}}'
        const rawData = JSON.parse(response);
        const formattedData = {};
        for (const [date, {
                Actual,
                Goal
            }] of Object.entries(rawData)) {
            formattedData[new Date(date).toLocaleDateString()] = {
                Actual,
                Goal
            };
        }
        stepsData = formattedData;

    } catch (e) {
        console.error(e);
        error = 'Error fetching data';
    }
}

onMount(async () => {

    await fetchData();

});
</script>

<main>
    {#if stepsData}
    <button on:click={toggleTable}>
        {#if showTable}
        Hide Table
        {:else}
        Show Table
        {/if}
    </button>
    {#if showTable}
    <div class="table-container">
        <h2>Steps Data</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Actual Steps</th>
                    <th>Goal Steps</th>
                </tr>
            </thead>
            <tbody>
                {#each Object.entries(stepsData) as [date, { Actual, Goal }]}
                <tr>
                    <td>{date}</td>
                    <td>{Actual}</td>
                    <td>{Goal}</td>
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
    {/if}

    {:else if error}
    <p>{error}</p>
    {:else}
    <p>Loading...</p>
    {/if}

</main>

<style>
main {
    font-family: Arial, sans-serif;
}

.table-container {
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 2px 2px 5px #ccc;
}

table {
    width: 100%;
    border-collapse: collapse;
}

thead th {
    text-align: left;
    background-color: #eee;
    padding: 10px;
}

tbody td {
    padding: 10px;
    border-bottom: 1px solid #ccc;
}

tbody td:first-of-type {
    font-weight: bold;
}

.plot-container {
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 2px 2px 5px #ccc;
}

.plot {
    width: 100%;
    height: 100%;
}

button {
    background-color: #0077c2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
}

button:hover {
    background-color: #005ca9;
}

button:active {
    background-color: #003d70;
}
</style>
