import React, { Component } from 'react';
import { Grid, Icon, Header, Segment } from 'semantic-ui-react';

class ZipStatus extends Component {

    render() {

        const statusIconDict = {
            0: <Icon name='times circle' size='big' color='red' />,
            1: <Icon name='warning sign' size='big' color='yellow' />,
            2: <Icon name='check circle' size='big' color='green' />,

        }

        const okToFlyDict = {
            0: <Icon name='times circle' size='big' color='red' />,
            1: <Icon name='check circle' size='big' color='green' />,
        }
        if (this.props.statusData) {
            return(
                <Segment>
                    <Grid columns={2} textAlign='center' verticalAlign='middle'>
                        <Grid.Row>
                            <Header>
                                <Header.Content>
                                    <Icon name='plane' size='huge'/>
                                    {this.props.statusData.zip_name}
                                </Header.Content>
                            </Header>
                        </Grid.Row>
                        <Grid.Row>
                            <Grid.Column>
                                <Header as='h3' content='Status' />
                                <Header as='h3' content={statusIconDict[this.props.statusData.status]} />
                            </Grid.Column>
                            <Grid.Column>
                                <Header as='h3' content='OK to Fly?' />
                                <Header as='h3' content={okToFlyDict[this.props.statusData.ok_to_fly]} />
                            </Grid.Column>
                        </Grid.Row>
                        <Grid.Row>
                            <Grid.Column>
                                <Header as='h3' content='# of Remaining Tasks' />
                                <Header as='h3' content={this.props.statusData.task_remain} />
                            </Grid.Column>
                            <Grid.Column>
                                <Header as='h3' content='# of Blocking Tasks' />
                                <Header as='h3' content={this.props.statusData.task_block} />
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            )
        }
        else {
            return null
        }
    }
}

export default ZipStatus;