

import { alpha } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Header from './components/Header';
import MainGrid from './components/MainGrid';
import AppTheme from './shared-theme/AppTheme';
import React, { useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import dayjs from 'dayjs';

import {
  chartsCustomizations,
  dataGridCustomizations,
  datePickersCustomizations,
  treeViewCustomizations,
} from './theme/customizations';

const xThemeComponents = {
  ...chartsCustomizations,
  ...dataGridCustomizations,
  ...datePickersCustomizations,
  ...treeViewCustomizations,
};

export default function Dashboard(props) {
  // state definition
  // --------------------
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState('upload')
 
  const [response, setResponse] = useState(
    {mean_cycle: '...',
      min_cycle: ['...', '...', '...'],
      max_cycle: ['...', '...', '...']
    });

  const [dateValue, setDateValue] = useState(null);
  // --------------------
  

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
     setUploadMessage('Please select a file');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setUploadMessage('Uploading...')

    try {
      const request = await axios.post('/upload', formData, {
        headers: {
          // No need to set 'Content-Type', axios will do it for us
        },
      });
      console.log('got response', request)

      setUploadMessage(`File uploaded successfully`);
      setResponse(request.data)
    } catch (error) {
      console.error('Upload error:', error);
      setUploadMessage('Error uploading file');
    } finally {
      setUploading(false);
      setDateValue(null)
    }
  };
  // Button upload handle
  function handleClick() {
    
  }

  // file handler
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      if (selectedFile.name.split('.').pop() !== 'csv'){

        setUploadMessage('only *csv files are allowed!')
        return
      }
      setFile(selectedFile);
    }
  };

  // time update handler
    const handleTimeUpdate = (val) => {
      console.log('checl val', val)
      setDateValue(val)
  
      var data = response
      setResponse(data)
      
    }

  return (
    <AppTheme {...props} themeComponents={xThemeComponents}>
      <CssBaseline enableColorScheme />
      <Box sx={{ display: 'flex' }}>
      
        <Box
          component="main"
          sx={(theme) => ({
            flexGrow: 1,
            backgroundColor: theme.vars
              ? `rgba(${theme.vars.palette.background.defaultChannel} / 1)`
              : alpha(theme.palette.background.default, 1),
            overflow: 'auto',
          })}
        >
          <Stack
            spacing={2}
            sx={{
              alignItems: 'center',
              mx: 3,
              pb: 5,
              mt: { xs: 8, md: 0 },
            }}
          >
            <Header date={dateValue} onClick={handleTimeUpdate}/>
            
            <MainGrid response={response} date={dateValue}/>
            <Stack spacing={3} direction="row">
            <form onSubmit={handleSubmit} encType="multipart/form-data">
              <Button variant="outlined">
              <input type="file" name="file" accept=".csv" onChange={handleFileChange} />
              </Button>
              <Button variant="outlined" type="submit" disabled={uploading} onClick={() => handleClick()}>

                {uploadMessage}
              </Button>
            </form>
          </Stack>

          </Stack>
        </Box>
      </Box>
    </AppTheme>
  );
}
