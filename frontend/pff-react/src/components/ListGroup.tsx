import {Button, Container, Typography} from '@mui/material';

export default function TestMUI() {
  return (
    <Container maxWidth="sm" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut aliquam neque sit amet dolor lacinia, non varius neque lacinia. Proin eu felis vel nunc eleifend porta ultricies non metus. Proin pellentesque, neque id auctor vulputate, elit massa pretium enim, non iaculis ligula dolor eu augue. Quisque nec ante porttitor, ultrices mauris at, fermentum velit. Proin viverra lobortis auctor. Praesent tincidunt mollis bibendum. Aenean non lacus sapien.

Integer neque mauris, blandit ut arcu a, luctus blandit erat. Nulla ac nisl nec lacus pellentesque auctor. Integer nec neque fringilla, congue orci eu, volutpat turpis. Donec aliquam accumsan sem id convallis. Sed tempus luctus justo, fringilla egestas lorem pellentesque eu. Nullam eu fringilla lacus. Phasellus ut purus consectetur, laoreet nulla eget, venenatis libero. Fusce diam tortor, mattis sit amet justo eget, fermentum pharetra risus. Sed laoreet dui non lectus condimentum, id gravida augue venenatis. Nullam maximus, est quis ullamcorper egestas, lorem nisi eleifend dui, eu molestie odio eros vitae lectus. Aliquam vitae mauris ante. Ut pretium malesuada ante sit amet elementum. Aliquam erat volutpat. Mauris non quam vitae sem tempus molestie eu in quam. Aliquam erat volutpat.

In tincidunt commodo massa vitae vulputate. Nullam maximus ligula non risus euismod vestibulum. Nulla malesuada libero leo, a scelerisque tortor sagittis at. Etiam arcu massa, eleifend a nulla non, vulputate viverra orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin vel vestibulum odio. Vivamus turpis dolor, lobortis eu urna nec, ornare suscipit nunc. Donec euismod nisi nisl, sit amet dictum ante varius ac. Sed faucibus leo id metus porta hendrerit. Curabitur mi neque, venenatis ut scelerisque vitae, posuere sodales neque. Aliquam eu tempus sem, quis tempus metus. Fusce in tortor sed libero elementum laoreet ut vel est. Sed facilisis, nunc eget venenatis egestas, nulla tortor vulputate tortor, vitae porta libero diam a tellus. Nunc aliquam velit ac nisi laoreet, quis rutrum ante mattis.
      </Typography>
      <Button variant="contained" color="primary">
        Click Me
      </Button>
    </Container>
  );
}

