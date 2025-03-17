import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { columns, rows } from '../internals/data/gridData';
import { experimentalStyled as styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid2';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import dayjs from 'dayjs';


export default function CustomizedDataGrid(props) {
  
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: 'center',
  color: theme.palette.text.secondary,
  ...theme.applyStyles('dark', {
    backgroundColor: '#1A2027',
  }),
}));

function reformatDate(time){
  console.log('time', time)
  var date = props.date
  if (date == null){
    return time
  } else {
    //console.log('time', time, date.valueOf(), dayjs(time + date.valueOf()).valueOf(), time+date.valueOf())
    let r_time = dayjs(time + date.valueOf())
    return String(r_time.format() + ' ' + r_time.millisecond())

  }
}

var response= {mean_cycle: '...',
      min_cycle: ['...', '...', '...'],
      max_cycle: ['...', '...', '...']
    };


  response = props.response
  return (

    <Box sx={{ flexGrow: 1 }}>

      <Grid container spacing={3}>
      <Grid size='grow'>
        <Item><b>Mean heart rate</b></Item>
      </Grid>
      <Grid size='grow'>
        <Item>{response.mean_cycle} bpm (beat per minute)</Item>
      </Grid>
      </Grid>
    <Grid container spacing={4} rowSpacing={1} columnSpacing={{ xs: 1,md: 1 }} >
      {/* {Array.from(Array(8)).map((_, index) => (
        <Grid key={index} size={{ xs: 3, md: 3 }}>
          <Item>{index + 1}</Item>
        </Grid>
      ))} */}

      <Grid key={0} size={{ xs: 3, md: 3 }} >
      <Item><b>Minimum Heart Rate</b></Item>
      </Grid>

      <Grid key={1} size={{ xs: 3, md: 3 }}>
      <Item>{response.min_cycle[0]} bpm</Item>
      </Grid>

      <Grid key={2} size={{ xs: 3, md: 3 }}>
      <Item>Starts at {reformatDate(response.min_cycle[1])} ms</Item>
      </Grid>
      <Grid key={3} size={{ xs: 3, md: 3 }}>
      <Item>Ends at {reformatDate(response.min_cycle[2])} ms</Item>
      </Grid>

      <Grid key={4} size={{ xs: 3, md: 3 }}>
      <Item><b>Maximum Heart Rate</b></Item>
      </Grid>
      <Grid key={5} size={{ xs: 3, md: 3 }}>
      <Item>{response.max_cycle[0]} bpm</Item>
      </Grid>
      <Grid key={6} size={{ xs: 3, md: 3 }}>
      <Item>Starts at {reformatDate(response.max_cycle[1])} ms</Item>
      </Grid>
      <Grid key={7} size={{ xs: 3, md: 3 }}>
      <Item>Ends at {reformatDate(response.max_cycle[2])} ms</Item>
      </Grid>
    </Grid>
  </Box>
    // <DataGrid
    //   checkboxSelection
    //   rows={rows}
    //   columns={columns}
    //   getRowClassName={(params) =>
    //     params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd'
    //   }
    //   initialState={{
    //     pagination: { paginationModel: { pageSize: 20 } },
    //   }}
    //   pageSizeOptions={[10, 20, 50]}
    //   disableColumnResize
    //   density="compact"
    //   slotProps={{
    //     filterPanel: {
    //       filterFormProps: {
    //         logicOperatorInputProps: {
    //           variant: 'outlined',
    //           size: 'small',
    //         },
    //         columnInputProps: {
    //           variant: 'outlined',
    //           size: 'small',
    //           sx: { mt: 'auto' },
    //         },
    //         operatorInputProps: {
    //           variant: 'outlined',
    //           size: 'small',
    //           sx: { mt: 'auto' },
    //         },
    //         valueInputProps: {
    //           InputComponentProps: {
    //             variant: 'outlined',
    //             size: 'small',
    //           },
    //         },
    //       },
    //     },
    //   }}
    // />
  );
}
