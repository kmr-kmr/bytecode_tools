from .constants import (
    CMP_OP, HAS_ARGUMENT, EXTENDED_ARG_NAME, FORMAT_VALUE_NAME,
    MAKE_FUNCTION_NAME, OPCODES_3_0, OPCODES_3_4, OPCODES_3_5, OPCODES_3_6,
    OPCODES_3_7,

    # Opcode flags
    HAS_COM, HAS_CONST, HAS_FREE, HAS_JREL, HAS_JABS, HAS_LOCAL,
    HAS_NAME, HAS_NARGS,

    # Opcodes classifications
    CMP_OPCODES, CONST_OPCODES, FREE_OPCODES, JREL_OPCODES,
    JABS_OPCODES, LOCAL_OPCODES, NAME_OPCODES, NARGS_OPCODES,

    PY_VERSION
)

MAKE_FUNCTION_FLAGS = ('defaults', 'kwdefaults', 'annotations', 'closure')


class Opcode:

    # Op code and name are fixed for a given instruction type, hence they would
    # be defined at class level.
    OPCODE = None
    OPCODE_NAME = None
    PYTHON_VERSION = None

    def __init__(
        self,
        offset,
        end,
        line,
        arg,
        arg_val,
        arg_repr,
        is_jump_target):

        self.offset = offset
        self.end = end
        self.line = line
        self.arg = arg
        self.arg_val = arg_val
        self.arg_repr = arg_repr
        self.is_jump_target = is_jump_target

    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def has_const(cls):
        return cls.OPCODE in CONST_OPCODES

    @classmethod
    def has_name(cls):
        return cls.OPCODE in NAME_OPCODES

    @classmethod
    def has_jrel(cls):
        return cls.OPCODE in JREL_OPCODES

    @classmethod
    def has_jabs(cls):
        return cls.OPCODE in JABS_OPCODES

    @classmethod
    def has_jump(cls):
        return cls.OPCODE in (JABS_OPCODES + JREL_OPCODES)

    @classmethod
    def has_local(cls):
        return cls.OPCODE in LOCAL_OPCODES

    @classmethod
    def has_free(cls):
        return cls.OPCODE in FREE_OPCODES

    @classmethod
    def has_nargs(cls):
        return cls.OPCODE in NARGS_OPCODES

    @classmethod
    def has_arg(cls):
        return cls.OPCODE >= HAS_ARGUMENT

    @classmethod
    def has_cmp(cls):
        return cls.OPCODE in CMP_OPCODES

    @classmethod
    def is_extended_arg(cls):
        return cls.OPCODE_NAME == EXTENDED_ARG_NAME

    @classmethod
    def is_format_value(cls):
        return cls.OPCODE_NAME == FORMAT_VALUE_NAME

    @classmethod
    def is_make_function(cls):
        return cls.OPCODE_NAME == MAKE_FUNCTION_NAME


class OpcodeClassFactory:

    opcodes_generated = False
    opcodes_version = None

    @classmethod
    def gen_opcode_classes(cls, python_version=PY_VERSION):
        # If they are already generated, then no need to do it again.
        if cls.opcodes_generated and cls.opcodes_version == python_version:

            return
        # If no version passed, then consider default python 3 opcodes.
        ops = globals().get(
            'OPCODES_%s_%s' % tuple(str(python_version).split('.')))

        globals()['OPCODE_MAPPER'] = ops
        for op_code, op_name in ops.items():
            op_cls = type(
                op_name,
                (Opcode, ),
                {
                    'OPCODE': op_code,
                    'OPCODE_NAME': op_nam,
                    'PYTHON_VERSION': python_version
                }
            )
            globals()[op_name] = op_cls

        cls.opcodes_generated = True
        cls.opcodes_version = python_version
