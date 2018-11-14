import React, { Component } from 'react';
import { Grid, Dropdown, Button } from 'semantic-ui-react';

import Service from '../services/fetch';

class NewTaskSegment extends Component {
    constructor(props) {
        super(props)
        this.state = {options: [], selected: []}
        this.columns = [
            { title: 'Task ID', field: 'task_id', width: 100 },
            { title: 'Resolved?', field: 'resolved', width: 150, formatter: 'tickCross', editor: true },
            { title: 'Not Blocking?', field: 'non_blocking', width: 150, formatter: 'tickCross' },
            { title: 'Problem', field: 'problem_name'},
        ]
        this.apiService = new Service()
        this.refreshOption = this.refreshOption.bind(this)
        this.onSelectChange = this.onSelectChange.bind(this)
        this.addNewTasks = this.addNewTasks.bind(this)
    }

    async refreshOption() {
        let options = []
        const response = await this.apiService.get('problems')
        if (response.status === 200) {
            for (let i=0;i<response.data.length;i++) {
                let option = {}
                option.key = response.data[i].id
                option.value = response.data[i].id
                option.text = response.data[i].name

                options.push(option)
            }
            this.setState({ options: options })
        }
    }

    async addNewTasks() {
        let body = {}
        body.zip_id = this.props.zipId
        body.prob_ids = this.state.selected
        const response = await this.apiService.post('tasks', body)
        if (response.status === 200) {
            this.setState({ selected: [] })
            this.props.refreshData(this.props.zipId)
        }
    }

    onSelectChange(e, {value}) {
        this.setState({ selected: value})
    }

    componentDidMount() {
        this.refreshOption()
    }



    render() {
        return(
                <Grid textAlign='center' verticalAlign='middle'>
                    <Grid.Row>
                        <Grid.Column width={13}>
                            <Dropdown
                                placeholder='Select a problem'
                                fluid
                                selection
                                multiple
                                search
                                value={this.state.selected}
                                options={this.state.options}
                                onChange={this.onSelectChange}
                            />
                        </Grid.Column>
                        <Grid.Column width={3}>
                            <Button icon='plus' color='red' size='medium' circular onClick={this.addNewTasks}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
        )
    }
}

export default NewTaskSegment;