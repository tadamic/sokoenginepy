#ifndef OCTOBAN_TESSELLATION_HPP_0FEA723A_C86F_6753_04ABD475F6FCA5FB
#define OCTOBAN_TESSELLATION_HPP_0FEA723A_C86F_6753_04ABD475F6FCA5FB

#include "tessellation.hpp"

namespace sokoengine {

///
/// Tessellation for Octoban.
///
class LIBSOKOENGINE_API OctobanTessellation : public Tessellation {
public:
  virtual const Directions& legal_directions() const override;
  virtual position_t neighbor_position(
    position_t position, const Direction& direction, size_t board_width,
    size_t board_height
  ) const override;
  virtual AtomicMove char_to_atomic_move (char input_chr) const override;
  virtual char atomic_move_to_char (const AtomicMove& atomic_move) const override;
  virtual CellOrientation cell_orientation(
    position_t position, size_t board_width, size_t board_height
  ) const override;

  virtual std::string str() const override;
  virtual std::string repr() const override;

protected:
  OctobanTessellation() = default;
  friend class Tessellation;
};

} // namespace sokoengine

#endif // HEADER_GUARD
