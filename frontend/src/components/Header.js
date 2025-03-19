import * as React from 'react';
import Stack from '@mui/material/Stack';
import CustomDatePicker from './CustomDatePicker';
import ColorModeIconDropdown from './../shared-theme/ColorModeIconDropdown';
import { Typography } from '@mui/material';


export default function Header(props) {
  return (
    <Stack
      direction="row"
      sx={{
        display: { xs: 'none', md: 'flex' },
        width: '100%',
        alignItems: { xs: 'flex-start', md: 'center' },
        justifyContent: 'space-between',
        maxWidth: { sm: '100%', md: '1700px' },
        left: '100%',
        pt: 1.5,
      }}
      spacing={2}
    >

      <Stack>
        <Typography>ECG TOOL</Typography>
      </Stack>
      <Stack direction="row" sx={{ gap: 1 }}>
        <CustomDatePicker date={props.date} onClick={props.onClick}/>
        <ColorModeIconDropdown />
      </Stack>
    </Stack>
  );
}
