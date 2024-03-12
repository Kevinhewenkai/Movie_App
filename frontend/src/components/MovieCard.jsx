import React from "react";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CommentIcon from '@mui/icons-material/Comment';
import { Stack } from "@mui/material";
import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import { useNavigate } from "react-router-dom";

function MovieCard(prop) {
  const navigate = useNavigate();
  return (
    <div style={{ margin: '5vh 5vw' }}>
      <Card style={{ maxWidth: 345, background: '#202021' }}>
        {
          prop.image
            ? <CardMedia
              height='300'
              component={"img"}
              image={prop.image}
              alt={'image of movie'}
              onClick={() => navigate('/movie')}
            ></CardMedia>
            : <CardMedia
              height='300'
              component={"img"}
              image={require('../image/noImage.png')}
              alt={'image of movie'}
              onClick={() => navigate('/movie')}
            ></CardMedia>

        }
        <CardContent>
          <Typography gutterBottom variant="h5" component="div" color={'white'} onClick={() => navigate('/movie')}>
            {prop.movie_name ? prop.movie_name : 'Unknown Movie Name'}
          </Typography>
        </CardContent>
        <CardActions>
          <Stack direction={'row'} spacing={3}>
            <Stack direction={'row'} spacing={1} onClick={() => navigate('/comments')}>
              <CommentIcon style={{ color: 'white' }} />
              <Typography gutterBottom variant="body2" component="div" color={'white'}>
                comment
              </Typography>
            </Stack>
            <Stack direction={'row'} spacing={1}>
              <LibraryAddIcon style={{ color: 'white' }} />
              <Typography gutterBottom variant="body2" component="div" color={'white'}>
                save
              </Typography>
            </Stack>
          </Stack>
        </CardActions>
      </Card>
    </div>
  )
}

export default MovieCard;
