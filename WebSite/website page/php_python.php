<?php
//-----------------------------------------------------------
// thie code introduced from following website
// PPython(PHP and Python).
//   (2012-15 http://code.google.com/p/ppython/)
//
// License: http://www.apache.org/licenses/LICENSE-2.0
//-----------------------------------------------------------

define("LAJP_IP", "127.0.0.1");     //Python port IP
define("LAJP_PORT", 21230);         //Python lisent IP

define("PARAM_TYPE_ERROR", 101);    //variable type error
define("SOCKET_ERROR", 102);        //SOCKET error
define("LAJP_EXCEPTION", 104);      //Python error

function ppython()
{
    //variable number
    $args_len = func_num_args();
    //variable array
    $arg_array = func_get_args();

    //variable cannot less 1
    if ($args_len < 1)
    {
        throw new Exception("[PPython Error] lapp_call function's arguments length < 1", PARAM_TYPE_ERROR);
    }
    //the first variable
    if (!is_string($arg_array[0]))
    {
        throw new Exception("[PPython Error] lapp_call function's first argument must be string \"module_name::function_name\".", PARAM_TYPE_ERROR);
    }


    if (($socket = socket_create(AF_INET, SOCK_STREAM, 0)) === false)
    {
        throw new Exception("[PPython Error] socket create error.", SOCKET_ERROR);
    }

    if (socket_connect($socket, LAJP_IP, LAJP_PORT) === false)
    {
        throw new Exception("[PPython Error] socket connect error.", SOCKET_ERROR);
    }

    $request = json_encode(Array('Text'=>$arg_array[0]));
    $req_len = count($arg_array);


    $send_len = 0;
    do
    {
        //send
        if (($sends = socket_write($socket, $request, strlen($request))) === false)
        {
            throw new Exception("[PPython Error] socket write error.", SOCKET_ERROR);
        }

        $send_len += $sends;
        $request = substr($request, $sends);

    }while ($send_len < $req_len);

    //receive
    $response = "";
    while(true)
    {
        $recv = "";
        if (($recv = socket_read($socket, 1400)) === false)
        {
            throw new Exception("[PPython Error] socket read error.", SOCKET_ERROR);
        }
        if ($recv == "")
        {
            break;
        }

        $response .= $recv;

        //echo "{$response}<br>";

    }

    //close
    socket_close($socket);

    $rsp_stat = substr($response, 0, 1);    //return type
    $rsp_msg = substr($response, 0);        //return info

    return $rsp_msg;
    
}
?>
