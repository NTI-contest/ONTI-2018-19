public class CannonAI : ICannonAI
{
    private double _left;
    private double _right;
    private double _target;

    public void SetTarget(double distance)
    {
        _target = distance;
        _left = 45;
        _right = 90;
    }

    public double GetShootAngle()
    {
        return (_right + _left) / 2;
    }

    public void FeedbackHitDistance(double distance)
    {
        if (distance > _target)
        {
            _left = GetShootAngle();
        }
        else
        {
            _right = GetShootAngle();
        }
    }
}
