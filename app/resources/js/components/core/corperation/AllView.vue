<template>
    <div>
        <NavbarComponent></NavbarComponent>

        <div class="wrapper-table">
         <div class="field">
            <h3 class="has-text-primary title is-3 center">Land</h3>
        </div>
             <div style="width: 700px">
         <a class="button is-success is-small is-pulled-right">
                <span class="icon is-small">
                <i class="fas fa-plus"></i>
                </span>
                <span @click.prevent="createCompany()">Create a company</span>
        </a>
        </div>
        <table class="table is-hoverable" style="width: 700px">
            <thead>
                <th>Land id</th>
                <th>Land level</th>
                <th>Buying cost</th>
                <th>Renting cost</th>
            </thead>
            <tbody>
               
            </tbody>
        </table>
        <br><br>
        <table class="table is-hoverable" style="width: 700px">
            <thead>
                <th>Corporation Name</th>
                <th>Current Balance</th>
                <th>Storage Capacity</th>
                <th>No. Employees</th>
            </thead>
            <tbody>
               
            </tbody>
        </table>
        </div>
    </div>
</template>

<script>
import NavbarComponent from '../../NavbarComponent'
export default {
    components: {
        NavbarComponent
    }
}
</script>
<style scoped>
.wrapper-table {
        margin: auto;
        width: 700px;
}

.center{
    font-weight: bold;
    text-transform: uppercase;
    margin: auto;
    padding: 10px 0px 20px 0px;
    width: 100px;
}
</style>