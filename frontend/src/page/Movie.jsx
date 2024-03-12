import React from "react";
import { Link, makeStyles, Rating, Stack } from "@mui/material";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Comment from "../components/Comment";

function Movie() {
  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "2vh" }}>
      <Stack direction={'row'} spacing={5}>
        {/* <img src={require("../image/test.jpeg")} alt="image" width="200" height="320"/> */}
        <Stack direction={'column'} spacing={1}>
          <Stack direction={'row'} spacing={1} style={{
            display: 'flex',
            alignItems: 'center',
            flexWrap: 'wrap',
          }}>
            <Typography gutterBottom variant="h4" component="span" color={'white'}>
              About Time
            </Typography>
            <Link href="#" variant="body1">
              2013
            </Link>
            <Typography gutterBottom variant="body2" component="div" color={'white'}>
              directed by
            </Typography>
            <Link href="#" variant="h5">
              Richard Curtis
            </Link>
          </Stack>
          <Card sx={{ maxWidth: 500, background: '#202021' }}>
            <CardContent>
              <Typography gutterBottom variant="body1" component="div" color={'white'}>
                WHAT IF EVERY MOMENT IN LIFE CAME WITH A SECOND CHANCE?
                <br />
                The night after another unsatisfactory New Year party, Tim’s father tells his son that the men in his family have always had the ability to travel through time. Tim can’t change history, but he can change what happens and has happened in his own life – so he decides to make his world a better place… by getting a girlfriend. Sadly, that turns out not to be as easy as he thinks.
              </Typography>
            </CardContent>
          </Card>
        </Stack>
        <Rating name="read-only" value={5} readOnly />
      </Stack>
    </div>
  )
}

export default Movie;
