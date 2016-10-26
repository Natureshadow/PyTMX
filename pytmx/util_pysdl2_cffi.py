"""
Copyright (C) 2012-2016

This file is part of pytmx.

pytmx is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pytmx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pytmx.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from functools import partial

logger = logging.getLogger(__name__)

try:
    import sdl
except ImportError:
    sdl = None
    logger.error('cannot import pysdl_cffi (is it installed?)')
    raise

__all__ = ('load_pysdl2_cffi', 'pysdl2_cffi_image_loader')

flag_names = (
    'flipped_horizontally',
    'flipped_vertically',
    'flipped_diagonally',)


def load_pysdl2_cffi(ctx, filename, *args, **kwargs):
    """ Load map and images using pysdl2_cffi

    :param ctx:
    :param filename:
    :param args:
    :param kwargs:

    :rtype: pytmx.TiledMap
    """
    import pytmx

    kwargs['image_loader'] = partial(pysdl2_cffi_image_loader, ctx)
    return pytmx.TiledMap(filename, *args, **kwargs)


def pysdl2_cffi_image_loader(ctx, filename, colorkey, **kwargs):
    """ Basic image loading with pysdl2_cffi

    Does not handle colorkey transparency

    :param ctx:
    :param filename:
    :param colorkey:
    :param kwargs:

    :return:
    """

    def load_image(rect=None, flags=None):
        if rect:
            try:
                flip = 0
                if flags.flipped_horizontally:
                    flip |= sdl.FLIP_HORIZONTAL
                if flags.flipped_vertically:
                    flip |= sdl.FLIP_VERTICAL
                if flags.flipped_diagonally:
                    flip |= 4

                this_rect = sdl.Rect()
                this_rect.x = rect[0]
                this_rect.y = rect[1]
                this_rect.w = rect[2]
                this_rect.h = rect[3]
                return texture, this_rect, flip

            except ValueError:
                logger.error('Tile bounds outside bounds of tileset image')
                raise
        else:
            return texture, None, 0

    texture = sdl.image.loadTexture(ctx.renderer, filename)

    # not sure if this is needed for normal map rendering operations
    # # by default use the alpha channel of the texture
    # if kwargs.get('pixelalpha', True):
    #     sdl.setTextureBlendMode(texture, sdl.BLENDMODE_BLEND)

    return load_image
