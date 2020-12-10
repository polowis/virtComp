<template>
    <div>
        <NavbarComponent></NavbarComponent>

        <div class="wrapper-table">
            <!--
         <div class="field">
            <h3 class="has-text-primary title is-3 center">Land</h3>
        </div>-->
        
        <!--
         <a class="button is-success is-small is-pulled-right">
                <span class="icon is-small">
                <i class="fas fa-plus"></i>
                </span>
                <span @click.prevent="createCompany()">Create a company</span>
        </a>-->
       
       <div style="margin-top: 30px;">
        <table class="table is-hoverable is-pulled-left" style="width: 450px; padding: 5px; flex: 50%;">
            <caption class="has-text-primary title is-4">Land Buying/Renting</caption>
            <thead>
                <th>Land id</th>
                <th>Land level</th>
                <th>Buying cost</th>
                <th>Renting cost</th>
            </thead>
            <tbody>
               
            </tbody>
        </table>
        </div>
        
        <div style="margin-top: 30px;">
        <table class="table is-hoverable is-pulled-right" style="width: 450px; padding: 5px; flex: 50%;">
            <caption class="has-text-primary title is-4">Build/Rent corp</caption>
            <thead>
                <th>Corp name</th>
                <th>Balance</th>
                <th>Storage</th>
                <th>Employees</th>
            </thead>
            <tbody>
               
            </tbody>
        </table>
        </div>
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
        width: 1000px;
}



.center{
    font-weight: bold;
    text-transform: uppercase;
    margin: auto;
    padding: 10px 0px 20px 0px;
    width: 100px;
}
</style>