let conf = in_channel "conf" in

let rec readlines c_chan lines =
  lines @ [(input_line c_chan)];
  readlines c_chan lines;
  lines;;

let 
