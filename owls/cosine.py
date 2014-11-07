import os
import sys
import string
import math

if __name__=="__main__": 
    input_vector = sys.argv[1:8]
    output_vector = sys.argv[8:15]

    in_sq = 0
    op_sq = 0
    for i in range(7) :
        input_vector[i] = int(input_vector[i])
        output_vector[i] = int(output_vector[i])
        in_sq += input_vector[i] * input_vector[i]
        op_sq += output_vector[i] * output_vector[i]

    in_sq = math.sqrt(in_sq)
    op_sq = math.sqrt(op_sq)

    ind_file = open("indexed_services.txt","r")

    for line in ind_file :
        text = line.split(':')
        inp_vec_text = string.translate(text[1].strip(), None, "\n").split()
        op_vec_text = string.translate(text[2].strip(), None, "\n").split()

        sq_in_text = 0
        sq_op_text = 0
        inp_sum = 0
        op_sum = 0
        in_cos = 0
        op_cos = 0

        for i in range(7) :
            inp_vec_text[i] = int(inp_vec_text[i])
            op_vec_text[i] = int(op_vec_text[i])
            inp_sum += inp_vec_text[i] * input_vector[i]
            op_sum += op_vec_text[i] * output_vector[i]
            sq_in_text += inp_vec_text[i] * inp_vec_text[i]
            sq_op_text += op_vec_text[i] * op_vec_text[i]

        sq_in_text = math.sqrt(sq_in_text)
        sq_op_text = math.sqrt(sq_op_text)
        den_in = sq_in_text * in_sq
        den_op = sq_op_text * op_sq

        if not den_in == 0 :
            in_cos = inp_sum / den_in
        if not den_op == 0:
            op_cos = op_sum / den_op

        print in_cos, op_cos

    ind_file.close()