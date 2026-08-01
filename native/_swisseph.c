/*
 * Minimal CPython binding used by Nataly.
 *
 * The astronomical calculations are provided by the bundled Swiss Ephemeris
 * C sources. This wrapper intentionally exposes only the API surface used by
 * Nataly instead of vendoring the complete pyswisseph binding.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>

#define NATALY_SERR_SIZE 256

/* Swiss Ephemeris public C API used by Nataly. */
extern double swe_julday(int year, int month, int day, double hour, int gregflag);
extern int32_t swe_calc_ut(
    double tjd_ut,
    int ipl,
    int32_t iflag,
    double *xx,
    char *serr
);
extern int swe_houses(
    double tjd_ut,
    double geolat,
    double geolon,
    int hsys,
    double *cusps,
    double *ascmc
);
extern void swe_set_ephe_path(char *path);
extern void swe_close(void);
extern char *swe_version(char *version_buffer);

static PyObject *NatalySwissEphError = NULL;

static PyObject *nataly_set_ephe_path(PyObject *self, PyObject *args) {
    const char *path = NULL;
    (void)self;

    if (!PyArg_ParseTuple(args, "s:set_ephe_path", &path)) {
        return NULL;
    }

    swe_set_ephe_path((char *)path);
    Py_RETURN_NONE;
}

static PyObject *nataly_close(PyObject *self, PyObject *Py_UNUSED(args)) {
    (void)self;
    swe_close();
    Py_RETURN_NONE;
}

static PyObject *nataly_julday(PyObject *self, PyObject *args) {
    int year = 0;
    int month = 0;
    int day = 0;
    int gregflag = 1;
    double hour = 0.0;
    (void)self;

    if (!PyArg_ParseTuple(
            args,
            "iiid|i:julday",
            &year,
            &month,
            &day,
            &hour,
            &gregflag)) {
        return NULL;
    }

    return PyFloat_FromDouble(swe_julday(year, month, day, hour, gregflag));
}

static PyObject *nataly_calc_ut(PyObject *self, PyObject *args) {
    double tjd_ut = 0.0;
    int body = 0;
    int flags = 260; /* SEFLG_SWIEPH | SEFLG_SPEED */
    double values[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    char error_message[NATALY_SERR_SIZE] = {0};
    int32_t return_flags = 0;
    PyObject *position = NULL;
    Py_ssize_t index = 0;
    (void)self;

    if (!PyArg_ParseTuple(args, "di|i:calc_ut", &tjd_ut, &body, &flags)) {
        return NULL;
    }

    return_flags = swe_calc_ut(
        tjd_ut,
        body,
        (int32_t)flags,
        values,
        error_message
    );

    if (return_flags < 0) {
        PyErr_SetString(
            NatalySwissEphError,
            error_message[0] != '\0'
                ? error_message
                : "Swiss Ephemeris calculation failed"
        );
        return NULL;
    }

    position = PyTuple_New(6);
    if (position == NULL) {
        return NULL;
    }

    for (index = 0; index < 6; ++index) {
        PyObject *value = PyFloat_FromDouble(values[index]);
        if (value == NULL) {
            Py_DECREF(position);
            return NULL;
        }
        PyTuple_SET_ITEM(position, index, value);
    }

    return Py_BuildValue("Ni", position, (int)return_flags);
}

static PyObject *nataly_houses(PyObject *self, PyObject *args) {
    double tjd_ut = 0.0;
    double geolat = 0.0;
    double geolon = 0.0;
    Py_buffer house_system = {0};
    double cusps[13] = {0.0};
    double ascmc[10] = {0.0};
    int result = 0;
    PyObject *python_cusps = NULL;
    PyObject *python_ascmc = NULL;
    Py_ssize_t index = 0;
    (void)self;

    if (!PyArg_ParseTuple(
            args,
            "dddy*:houses",
            &tjd_ut,
            &geolat,
            &geolon,
            &house_system)) {
        return NULL;
    }

    if (house_system.len != 1) {
        PyBuffer_Release(&house_system);
        PyErr_SetString(
            PyExc_ValueError,
            "house system must be exactly one byte"
        );
        return NULL;
    }

    result = swe_houses(
        tjd_ut,
        geolat,
        geolon,
        (int)((unsigned char *)house_system.buf)[0],
        cusps,
        ascmc
    );
    PyBuffer_Release(&house_system);

    if (result < 0) {
        PyErr_SetString(
            NatalySwissEphError,
            "Swiss Ephemeris house calculation failed"
        );
        return NULL;
    }

    /*
     * Swiss Ephemeris uses cusp indexes 1..12. pyswisseph historically
     * returns a 12-item tuple indexed 0..11, which is what Nataly expects.
     */
    python_cusps = PyTuple_New(12);
    python_ascmc = PyTuple_New(8);
    if (python_cusps == NULL || python_ascmc == NULL) {
        Py_XDECREF(python_cusps);
        Py_XDECREF(python_ascmc);
        return NULL;
    }

    for (index = 0; index < 12; ++index) {
        PyObject *value = PyFloat_FromDouble(cusps[index + 1]);
        if (value == NULL) {
            Py_DECREF(python_cusps);
            Py_DECREF(python_ascmc);
            return NULL;
        }
        PyTuple_SET_ITEM(python_cusps, index, value);
    }

    for (index = 0; index < 8; ++index) {
        PyObject *value = PyFloat_FromDouble(ascmc[index]);
        if (value == NULL) {
            Py_DECREF(python_cusps);
            Py_DECREF(python_ascmc);
            return NULL;
        }
        PyTuple_SET_ITEM(python_ascmc, index, value);
    }

    return Py_BuildValue("NN", python_cusps, python_ascmc);
}

static PyMethodDef NatalySwissEphMethods[] = {
    {
        "set_ephe_path",
        nataly_set_ephe_path,
        METH_VARARGS,
        "Set the Swiss Ephemeris data directory."
    },
    {
        "close",
        nataly_close,
        METH_NOARGS,
        "Release Swiss Ephemeris resources."
    },
    {
        "julday",
        nataly_julday,
        METH_VARARGS,
        "Convert a calendar date to Julian day."
    },
    {
        "calc_ut",
        nataly_calc_ut,
        METH_VARARGS,
        "Calculate a body position for a UT Julian day."
    },
    {
        "houses",
        nataly_houses,
        METH_VARARGS,
        "Calculate house cusps and chart angles."
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef NatalySwissEphModule = {
    PyModuleDef_HEAD_INIT,
    "_swisseph",
    "Minimal Swiss Ephemeris binding bundled with Nataly.",
    -1,
    NatalySwissEphMethods
};

static int add_int_constant(PyObject *module, const char *name, long value) {
    return PyModule_AddIntConstant(module, name, value);
}

PyMODINIT_FUNC PyInit__swisseph(void) {
    PyObject *module = PyModule_Create(&NatalySwissEphModule);
    char version_buffer[64] = {0};

    if (module == NULL) {
        return NULL;
    }

    NatalySwissEphError = PyErr_NewException(
        "nataly._swisseph.Error",
        NULL,
        NULL
    );
    if (NatalySwissEphError == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(NatalySwissEphError);
    if (PyModule_AddObject(module, "Error", NatalySwissEphError) < 0) {
        Py_DECREF(NatalySwissEphError);
        Py_DECREF(module);
        return NULL;
    }

    swe_version(version_buffer);
    if (PyModule_AddStringConstant(module, "version", version_buffer) < 0 ||
        PyModule_AddStringConstant(module, "__version__", version_buffer) < 0) {
        Py_DECREF(module);
        return NULL;
    }

#define ADD_CONSTANT(name, value) \
    if (add_int_constant(module, name, value) < 0) { \
        Py_DECREF(module); \
        return NULL; \
    }

    ADD_CONSTANT("SUN", 0);
    ADD_CONSTANT("MOON", 1);
    ADD_CONSTANT("MERCURY", 2);
    ADD_CONSTANT("VENUS", 3);
    ADD_CONSTANT("MARS", 4);
    ADD_CONSTANT("JUPITER", 5);
    ADD_CONSTANT("SATURN", 6);
    ADD_CONSTANT("URANUS", 7);
    ADD_CONSTANT("NEPTUNE", 8);
    ADD_CONSTANT("PLUTO", 9);
    ADD_CONSTANT("MEAN_NODE", 10);
    ADD_CONSTANT("TRUE_NODE", 11);
    ADD_CONSTANT("CHIRON", 15);
    ADD_CONSTANT("PHOLUS", 16);
    ADD_CONSTANT("CERES", 17);
    ADD_CONSTANT("PALLAS", 18);
    ADD_CONSTANT("JUNO", 19);
    ADD_CONSTANT("VESTA", 20);

    /* ascmc indexes used by Nataly. */
    ADD_CONSTANT("ASC", 0);
    ADD_CONSTANT("MC", 1);

    ADD_CONSTANT("FLG_JPLEPH", 1);
    ADD_CONSTANT("FLG_SWIEPH", 2);
    ADD_CONSTANT("FLG_MOSEPH", 4);
    ADD_CONSTANT("FLG_SPEED", 256);
    ADD_CONSTANT("FLG_EQUATORIAL", 2048);
    ADD_CONSTANT("GREG_CAL", 1);
    ADD_CONSTANT("JUL_CAL", 0);

#undef ADD_CONSTANT

    return module;
}
