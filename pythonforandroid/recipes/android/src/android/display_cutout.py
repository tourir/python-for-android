from jnius import autoclass
from kivy.core.window import Window

from android import mActivity

__all__ = ('get_cutout_pos', 'get_cutout_size', 'get_width_of_bar',
           'get_height_of_bar', 'get_size_of_bar', 'get_width_of_bar',
           'get_cutout_mode')


def _core_cutout():
    decorview = mActivity.getWindow().getDecorView()
    cutout = decorview.rootWindowInsets.displayCutout

    return cutout.boundingRects.get(0)


def get_cutout_pos():
    """Get position of the display-cutout.
       Returns integer for each positions (xy)
    """
    try:
        cutout = _core_cutout()
        return int(cutout.left), int(Window.height - cutout.height())
    except Exception:
        # Doesn't have a camera builtin with the display
        return 0, 0


def get_cutout_size():
    """Get the size (xy) of the front camera.
       Returns size with float values
    """
    try:
        cutout = _core_cutout()
        return float(cutout.width()), float(cutout.height())
    except Exception:
        # Doesn't have a camera builtin with the display
        return 0., 0.


def get_height_of_bar(bar_target=None):
    """Get the height of either statusbar or navigationbar
       bar_target = status or navigation and defaults to status
    """
    bar_target = bar_target or 'status'

    if bar_target not in ('status', 'navigation'):
        raise Exception("bar_target must be 'status' or 'navigation'")

    try:
        displayMetrics = autoclass('android.util.DisplayMetrics')
        mActivity.getWindowManager().getDefaultDisplay().getMetrics(displayMetrics())
        resources = mActivity.getResources()
        resourceId = resources.getIdentifier(f'{bar_target}_bar_height', 'dimen',
                                             'android')

        return float(max(resources.getDimensionPixelSize(resourceId), 0))
    except Exception:
        # Getting the size is not supported on older Androids
        return 0.


def get_width_of_bar(bar_target=None):
    """Get the width of the bar"""
    return Window.width


def get_size_of_bar(bar_target=None):
    """Get the size of either statusbar or navigationbar
       bar_target = status or navigation and defaults to status
    """
    return get_width_of_bar(), get_height_of_bar(bar_target)


def get_heights_of_both_bars():
    """Return heights of both bars"""
    return get_height_of_bar('status'), get_height_of_bar('navigation')


def get_cutout_mode():
    """Return mode for cutout supported applications"""
    BuildVersion = autoclass('android.os.Build$VERSION')
    cutout_modes = {}

    if BuildVersion.SDK_INT >= 28:
        LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
        window = mActivity.getWindow()
        layout_params = window.getAttributes()
        cutout_mode = layout_params.layoutInDisplayCutoutMode
        cutout_modes.update({LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_DEFAULT: 'default',
                             LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES: 'shortEdges'})

        if BuildVersion.SDK_INT >= 30:
            cutout_modes[LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS] = 'always'

        return cutout_modes.get(cutout_mode, 'never')

    return None
